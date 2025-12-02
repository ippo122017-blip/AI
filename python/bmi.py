try:
    height=float(input("身長をcmで入力してください:"))
    weight=float(input("体重をkgで入力してください:"))

    bmi=weight/(height/100)**2

    print("あなたのBMIは",round(bmi,1),"です。")

    if bmi < 18.5:
        print("痩せ気味です。")

    elif bmi<25:
        print("標準")
    else:
        print("肥満") 

except ValueError:
    print("数字で入力しなさい")

except ZeroDivisionError:
    print("身長は0より大きい値だろばか")



