# Function returning list
def even_numbers(limit):
    return [x for x in range(limit+1) if x%2 ==0]
print(even_numbers(10))
