list1 = [] 
list2 = [] 
  
# Index ranges from 1 to 10 to multiply 
for i in range(1,11): 
    list1.append(4*i)  
  
# Index to access the list2 is from 0 to 9 
for i in range(0,10): 
    list2 = [x%5==0 for x in list1]
    # list2.append(list1[i]%6==0) 

print(list1)
print(list2)
print('See whether at least one number is divisible by 5 in list 1=>') 
print(all([True, True, False]))

print(int(round(0.663)))