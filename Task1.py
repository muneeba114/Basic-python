#Question 01: Variable Mutability (Price Override)
#Ek product ki initial price discount_price = 1500 set ki gayi hai.
#Black Friday sale khatam hone par aapko is variable ki value ko update karke original_price = 2000 ke barabar assign karna hai.
#Assignment operator ka use karke value update karein aur updated price print karein.

discount_price = 1500
original_price = 2000
discount_price = original_price
print("Updated Price:", discount_price)
