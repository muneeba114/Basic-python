# Ek online pizza delivery app ke liye, user se pizza ka diameter input lein. Is diameter ka use karte hue pizza ka total area calculate karein:
#  Area = 3.14 × (diameter / 2)2 
# User se input lete waqt typecasting ka khyal rakhein kyunki input hamesha string return karta hai.
diameter = float(input("Enter The Diameter of the pizza in inches:"))
area = 3.14 * (diameter / 2) **2
print("\n--- Pizza Order Details ---")
print(f"Pizza Diameter: {diameter} inches")
print(f"Pizza ka Total Area: {round(area, 2)} square inches")

