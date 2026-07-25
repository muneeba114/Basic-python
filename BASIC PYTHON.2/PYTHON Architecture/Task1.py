# Ek traffic signal automation script likhein jo user se light ka current color 
# ("Red", "Yellow", "Green") as input le. Agar light "Red" ho to "Stop your vehicle", agar "Yellow" ho to "Slow Down", aur agar "Green" ho to "Go" print kare.
light_colour=input("enter the colour:")
if light_colour=="Red":
    print("stop vehicle")
elif light_colour=="yellow":
    print("slow down")
elif light_colour=="green":
    print("go")
else:
    print("invalid colour")
    