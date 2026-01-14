''' For multiple return values
'''
def calcuate(a, b):
    return a+b,a*b
sum_, product_= calcuate(4,5)
print(sum_,product_)