#car rental management sytem
import sqlite3
from datetime import datetime

class RentalDatabase:
    """Handles connection and SQL operations for the rental system."""
    def __init__(self, db_name="car_rental.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Cars Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                daily_rate REAL NOT NULL,
                status TEXT DEFAULT 'AVAILABLE'
            )
        ''')
        # Customers Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        # Rentals Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                customer_id INTEGER,
                rental_days INTEGER NOT NULL,
                rental_date TEXT NOT NULL,
                total_cost REAL,
                status TEXT DEFAULT 'ACTIVE',
                FOREIGN KEY(car_id) REFERENCES cars(car_id),
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()


class CarRentalSystem:
    """Handles business logic for fleet management and rentals."""
    def __init__(self, db):
        self.db = db

    def add_car(self, make, model, daily_rate):
        self.db.cursor.execute(
            "INSERT INTO cars (make, model, daily_rate) VALUES (?, ?, ?)",
            (make, model, daily_rate)
        )
        self.db.conn.commit()
        print(f"\n✅ {make} {model} added to fleet (${daily_rate:.2f}/day).")

    def register_customer(self, name, phone):
        self.db.cursor.execute(
            "INSERT INTO customers (name, phone) VALUES (?, ?)",
            (name, phone)
        )
        self.db.conn.commit()
        cust_id = self.db.cursor.lastrowid
        print(f"\n✅ Customer '{name}' registered successfully! Customer ID: {cust_id}")

    def display_fleet(self, available_only=False):
        query = "SELECT * FROM cars WHERE status = 'AVAILABLE'" if available_only else "SELECT * FROM cars"
        self.db.cursor.execute(query)
        cars = self.db.cursor.fetchall()

        print("\n" + "="*55)
        title = "AVAILABLE CARS" if available_only else "ALL FLEET VEHICLES"
        print(title.center(55))
        print("="*55)
        if not cars:
            print("No vehicles match the selected criteria.")
            return

        print(f"{'ID':<5} {'Make':<15} {'Model':<15} {'Rate/Day':<12} {'Status'}")
        print("-" * 55)
        for c in cars:
            print(f"{c[0]:<5} {c[1]:<15} {c[2]:<15} ${c[3]:<11.2f} {c[4]}")

    def rent_car(self, car_id, customer_id, days):
        # Validate Car
        self.db.cursor.execute("SELECT make, model, daily_rate, status FROM cars WHERE car_id = ?", (car_id,))
        car = self.db.cursor.fetchone()

        if not car:
            print("\n❌ Error: Car ID not found.")
            return
        if car[3] != 'AVAILABLE':
            print(f"\n❌ Error: {car[0]} {car[1]} is currently RENTED.")
            return

        # Validate Customer
        self.db.cursor.execute("SELECT name FROM customers WHERE customer_id = ?", (customer_id,))
        customer = self.db.cursor.fetchone()
        if not customer:
            print("\n❌ Error: Customer ID not found.")
            return

        total_cost = car[2] * days
        rental_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Create Rental Record
        self.db.cursor.execute(
            "INSERT INTO rentals (car_id, customer_id, rental_days, rental_date, total_cost) VALUES (?, ?, ?, ?, ?)",
            (car_id, customer_id, days, rental_date, total_cost)
        )
        # Update Car Status
        self.db.cursor.execute("UPDATE cars SET status = 'RENTED' WHERE car_id = ?", (car_id,))
        self.db.conn.commit()

        rental_id = self.db.cursor.lastrowid
        print("\n" + "="*45)
        print("🎉 RENTAL AGREEMENT CONFIRMED".center(45))
        print("="*45)
        print(f" Rental ID   : #{rental_id}")
        print(f" Customer    : {customer[0]}")
        print(f" Vehicle     : {car[0]} {car[1]}")
        print(f" Duration    : {days} Days")
        print(f" Total Bill  : ${total_cost:.2f}")
        print("="*45)

    def return_car(self, rental_id):
        self.db.cursor.execute(
            "SELECT car_id, status FROM rentals WHERE rental_id = ?", (rental_id,)
        )
        record = self.db.cursor.fetchone()

        if not record:
            print("\n❌ Error: Rental Transaction ID not found.")
            return
        if record[1] == 'COMPLETED':
            print("\n❌ Error: This rental has already been marked as returned.")
            return

        car_id = record[0]
        # Close Rental
        self.db.cursor.execute("UPDATE rentals SET status = 'COMPLETED' WHERE rental_id = ?", (rental_id,))
        # Set Car back to Available
        self.db.cursor.execute("UPDATE cars SET status = 'AVAILABLE' WHERE car_id = ?", (car_id,))
        self.db.conn.commit()
        print(f"\n✅ Rental #{rental_id} closed! Car ID {car_id} is now available in fleet.")

    def view_active_rentals(self):
        self.db.cursor.execute('''
            SELECT r.rental_id, c.name, k.make, k.model, r.rental_days, r.total_cost, r.rental_date
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN cars k ON r.car_id = k.car_id
            WHERE r.status = 'ACTIVE'
        ''')
        records = self.db.cursor.fetchall()

        print("\n" + "="*65)
        print("CURRENT ACTIVE RENTALS".center(65))
        print("="*65)
        if not records:
            print("No cars are currently out on rent.")
            return

        print(f"{'Rent ID':<8} {'Customer':<15} {'Vehicle':<20} {'Days':<6} {'Total Cost'}")
        print("-" * 65)
        for r in records:
            vehicle = f"{r[2]} {r[3]}"
            print(f"#{r[0]:<7} {r[1]:<15} {vehicle:<20} {r[4]:<6} ${r[5]:.2f}")


# Interactive CLI Menu
def main():
    db = RentalDatabase()
    system = CarRentalSystem(db)

    while True:
        print("\n" + "="*40)
        print("🚗 CAR RENTAL MANAGEMENT SYSTEM".center(40))
        print("="*40)
        print("1. Display Available Cars")
        print("2. Rent a Car")
        print("3. Return a Car")
        print("4. Add New Vehicle to Fleet")
        print("5. Register New Customer")
        print("6. View Active Rental Agreements")
        print("7. Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == '1':
            system.display_fleet(available_only=True)
        elif choice == '2':
            system.display_fleet(available_only=True)
            try:
                car_id = int(input("\nEnter Car ID to Rent: "))
                cust_id = int(input("Enter Customer ID: "))
                days = int(input("Enter Rental Duration (Days): "))
                if days <= 0:
                    print("\n❌ Rental days must be greater than 0.")
                    continue
                system.rent_car(car_id, cust_id, days)
            except ValueError:
                print("\n❌ Input must be a valid integer.")
        elif choice == '3':
            try:
                rental_id = int(input("\nEnter Rental Agreement ID to Return: "))
                system.return_car(rental_id)
            except ValueError:
                print("\n❌ Input must be a valid integer.")
        elif choice == '4':
            make = input("Enter Car Make (e.g., Toyota): ").strip()
            model = input("Enter Car Model (e.g., Camry): ").strip()
            rate = float(input("Enter Daily Rental Rate ($): "))
            system.add_car(make, model, rate)
        elif choice == '5':
            name = input("Enter Customer Full Name: ").strip()
            phone = input("Enter Customer Phone Number: ").strip()
            system.register_customer(name, phone)
        elif choice == '6':
            system.view_active_rentals()
        elif choice == '7':
            print("\nShutting down system. Goodbye!")
            db.close()
            break
        else:
            print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()