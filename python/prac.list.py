list1=[]
for i in range(5):
    list1.append(int(input()))


for i in range(5):
    print(f"{i+1}番目は{list1[i]}です")
    
print("合計は",sum(list1),"要素は",len(list1))
