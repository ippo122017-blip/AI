try:
    height_cm = float(input("Enter height in cm: "))
    weight_kg = float(input("Enter weight in kg: "))

    bmi = weight_kg / (height_cm / 100) ** 2  # BMI = kg / m^2
    print(f"Your BMI is {bmi:.1f}")

    if bmi < 18.5:
        print("Category: Underweight")
    elif bmi < 25:
        print("Category: Normal range")
    else:
        print("Category: Overweight")

except ValueError:
    print("Please enter numbers only.")
except ZeroDivisionError:
    print("Height must be greater than zero.")
