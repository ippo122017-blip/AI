height = float(input("身長(m): "))
weight = float(input("体重(kg): "))

bmi = weight / height ** 2
if bmi < 18.5:
    category = "痩せ気味です"
elif bmi < 25:
    category = "普通体重です"
else:
    category = "太り気味です"

print(f"身長: {height} m, 体重: {weight} kg")
print(f"あなたのBMIは {bmi:.1f} で、{category}")
