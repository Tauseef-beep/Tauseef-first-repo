# Local variable  are the variables which are inside the function and 
#Global variables are the variables which are outside the function
x=10
def show():
    print('Inside',x)
show()
print('Outside ', x)
''' Global keyword Example '''
x=10
def modify ():
    global x
    x=20
modify()
print(x)