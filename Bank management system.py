# Bank management sytem
import sqlite3
import random
from datetime import datetime

class BankDatabase:
    """Handles connection and queries for SQLite database."""
    def __init__(self, db_name="bank.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Accounts Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance REAL DEFAULT 0.0
            )
        ''')
        # Transactions History Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_no INTEGER,
                trans_type TEXT,
                amount REAL,
                timestamp TEXT,
                FOREIGN KEY(account_no) REFERENCES accounts(account_no)
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()


class BankSystem:
    """Handles core banking operations."""
    def __init__(self, db):
        self.db = db

    def generate_acc_number(self):
        """Generates a random unique 6-digit account number."""
        while True:
            acc_no = random.randint(100000, 999999)
            self.db.cursor.execute("SELECT 1 FROM accounts WHERE account_no = ?", (acc_no,))
            if not self.db.cursor.fetchone():
                return acc_no

    def log_transaction(self, acc_no, trans_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.cursor.execute(
            "INSERT INTO transactions (account_no, trans_type, amount, timestamp) VALUES (?, ?, ?, ?)",
            (acc_no, trans_type, amount, timestamp)
        )

    def create_account(self, name, pin, initial_deposit):
        acc_no = self.generate_acc_number()
        self.db.cursor.execute(
            "INSERT INTO accounts (account_no, name, pin, balance) VALUES (?, ?, ?, ?)",
            (acc_no, name, pin, initial_deposit)
        )
        self.log_transaction(acc_no, "INITIAL DEPOSIT", initial_deposit)
        self.db.conn.commit()
        print("\n" + "="*45)
        print("🎉 ACCOUNT CREATED SUCCESSFULLY!".center(45))
        print("="*45)
        print(f" Account Holder : {name}")
        print(f" Account Number : {acc_no}")
        print(f" Balance        : ${initial_deposit:.2f}")
        print("="*45)

    def authenticate(self, acc_no, pin):
        self.db.cursor.execute("SELECT name, balance FROM accounts WHERE account_no = ? AND pin = ?", (acc_no, pin))
        return self.db.cursor.fetchone()

    def deposit(self, acc_no, amount):
        self.db.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_no = ?", (amount, acc_no))
        self.log_transaction(acc_no, "DEPOSIT", amount)
        self.db.conn.commit()
        print(f"\n✅ Successfully deposited ${amount:.2f}")

    def withdraw(self, acc_no, amount, current_balance):
        if amount > current_balance:
            print("\n❌ Error: Insufficient funds!")
            return False
        self.db.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_no = ?", (amount, acc_no))
        self.log_transaction(acc_no, "WITHDRAWAL", amount)
        self.db.conn.commit()
        print(f"\n✅ Successfully withdrew ${amount:.2f}")
        return True

    def transfer(self, sender_acc, receiver_acc, amount, sender_balance):
        # Check if receiver account exists
        self.db.cursor.execute("SELECT name FROM accounts WHERE account_no = ?", (receiver_acc,))
        receiver = self.db.cursor.fetchone()
        if not receiver:
            print("\n❌ Error: Destination account not found.")
            return

        if amount > sender_balance:
            print("\n❌ Error: Insufficient balance for transfer.")
            return

        # Deduct from sender, add to receiver
        self.db.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_no = ?", (amount, sender_acc))
        self.db.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_no = ?", (amount, receiver_acc))
        
        self.log_transaction(sender_acc, f"TRANSFER TO {receiver_acc}", amount)
        self.log_transaction(receiver_acc, f"TRANSFER FROM {sender_acc}", amount)
        
        self.db.conn.commit()
        print(f"\n✅ Successfully transferred ${amount:.2f} to Account #{receiver_acc} ({receiver[0]})")

    def display_statement(self, acc_no):
        self.db.cursor.execute("SELECT trans_type, amount, timestamp FROM transactions WHERE account_no = ? ORDER BY trans_id DESC", (acc_no,))
        records = self.db.cursor.fetchall()
        print("\n" + "="*50)
        print(f"TRANSACTION STATEMENT - ACC #{acc_no}".center(50))
        print("="*50)
        print(f"{'Date/Time':<22} {'Type':<18} {'Amount'}")
        print("-" * 50)
        for r in records:
            print(f"{r[2]:<22} {r[0]:<18} ${r[1]:.2f}")


# Interactive CLI Menu
def main():
    db = BankDatabase()
    bank = BankSystem(db)

    while True:
        print("\n" + "="*40)
        print("🏦 WELCOME TO PYTHON COMMUNITY BANK".center(40))
        print("="*40)
        print("1. Create New Account")
        print("2. Login to Account")
        print("3. Exit System")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == '1':
            name = input("Enter your full name: ").strip()
            pin = input("Set a 4-digit PIN: ").strip()
            deposit = float(input("Enter initial deposit amount ($): "))
            bank.create_account(name, pin, deposit)

        elif choice == '2':
            try:
                acc_no = int(input("Enter Account Number: "))
            except ValueError:
                print("\n❌ Account number must be numeric.")
                continue
            pin = input("Enter 4-digit PIN: ").strip()

            user = bank.authenticate(acc_no, pin)
            if user:
                print(f"\n👋 Welcome back, {user[0]}!")
                while True:
                    # Fetch real-time balance
                    db.cursor.execute("SELECT balance FROM accounts WHERE account_no = ?", (acc_no,))
                    balance = db.cursor.fetchone()[0]

                    print("\n--- ACCOUNT MENU ---")
                    print(f"Current Balance: ${balance:.2f}")
                    print("1. Deposit Funds")
                    print("2. Withdraw Funds")
                    print("3. Transfer Funds")
                    print("4. View Statement")
                    print("5. Logout")

                    acc_choice = input("\nChoose operation (1-5): ").strip()

                    if acc_choice == '1':
                        amt = float(input("Enter deposit amount ($): "))
                        if amt > 0:
                            bank.deposit(acc_no, amt)
                        else:
                            print("\n❌ Deposit must be positive.")
                    elif acc_choice == '2':
                        amt = float(input("Enter withdrawal amount ($): "))
                        if amt > 0:
                            bank.withdraw(acc_no, amt, balance)
                        else:
                            print("\n❌ Amount must be positive.")
                    elif acc_choice == '3':
                        target = int(input("Enter recipient Account Number: "))
                        amt = float(input("Enter transfer amount ($): "))
                        if amt > 0:
                            bank.transfer(acc_no, target, amt, balance)
                    elif acc_choice == '4':
                        bank.display_statement(acc_no)
                    elif acc_choice == '5':
                        print("\nLogged out successfully.")
                        break
                    else:
                        print("\n❌ Invalid option.")
            else:
                print("\n❌ Invalid Account Number or PIN!")

        elif choice == '3':
            print("\nThank you for banking with us. Goodbye!")
            db.close()
            break
        else:
            print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()