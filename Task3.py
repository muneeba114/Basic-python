# Aapko check karna hai ke system memory mein ek variable session_token = "XYZ789" kis address/location par store hua hai. 
# Aap is location ko check karne ke liye kis function ka use karenge?

session_token = "XYZ789"
mem_address_dec  = id(session_token)
mem_address_hex = hex(id(session_token))
print(f"Variable Value: {session_token}")
print(f"Memory Address (Decimal): {mem_address_dec}")
print(f"Memory Address (Hexadecimal): {mem_address_hex}")
