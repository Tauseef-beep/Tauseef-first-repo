#Check if the number is even or not
def is_prime(num):
    for i in range(2,num):
        if num%i==0:
            return False
        return True
print(is_prime(11))
# Now we will reverse string the process
def reverse(text):
    return text[::-1]
print(reverse('Python'))