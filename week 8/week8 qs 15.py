# Exercise 1 Question
# write the function to find the area of the rectangle
def rectangle_area_perimeter(length, width):
    area = length * width
    perimeter = 2 * (length + width)
    return area, perimeter

# Example usage
area, perimeter = rectangle_area_perimeter(5, 3)
print("Area:", area)
print("Perimeter:", perimeter)
# Exercise 2 Question
# Return the sum of even numbers
def sum_even_numbers(numbers):
    total = 0
    for num in numbers:
        if num % 2 == 0:
            total += num
    return total
''' Exercise 3 check if this palindrome or not'''
# Example
print(sum_even_numbers([1, 2, 3, 4, 5, 6]))
# Function to check palindrome
def is_palindrome(s):
    # Convert to lowercase to ignore case
    s = s.lower()
    # Check if string is equal to its reverse
    if s == s[::-1]:
        return True
    else:
        return False

# Example usage
word = input("Enter a word or number: ")
if is_palindrome(word):
    print(word, "is a palindrome")
else:
    print(word, "is not a palindrome")


