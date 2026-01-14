#Remove the elements through the list
fruits=['apple','banana','cherry','grape']
fruits.remove('banana')
print(fruits)
fruits.pop(1)
print(fruits)
del fruits[0]
print(fruits)
fruits.clear()
print(fruits)
#Looping through the list 
for fruit in fruits:
    print(fruit)
