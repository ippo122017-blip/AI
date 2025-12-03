print("数字を入力してください")
number1=float(input())
number2=float(input())


print("合計は",number1+number2)
print("差は",number1-number2)
print("積は",number1*number2)
if number2==0:
    print("商は計算不能")
else:
    print("商は",number1/number2)
