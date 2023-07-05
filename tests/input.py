a : int = 1
b : int = 3
maximum : int = 0
if (a > b):
    maximum = a
elif (b > a):
    maximum = b
else:
    for i in range(1, 10, 5):
        a += maximum

print("hellow")