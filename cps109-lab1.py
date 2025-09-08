from math import sqrt

'''
Task 1
'''

# read: str = input("Input Celcius: ")
# celcius: float = float(read)

# try:
#     f: float = celcius * (9/5) + 32
#     k = celcius + 273.15
#     print(f"Farenheit: {f}; Kelvin: {k}")

# except TypeError:
#     print("Type conversion warning")

'''
Task 2
'''

# input should be in order of a, b, c
# read: str = input("Input 3 numbers seperated by a space: ")
# rawValues: list[str] = read.split(" ")
# values: list[str] = []
# [values.append(float(x)) for x in rawValues]

# divisor: float = 2 * (values[0])

# # Discriminator calculation (+)
# a, b, c = values
# def discrim(sign: int) -> float | str:
#     val: float|str = (sign * values[1])
#     try:
#         calc: float = sqrt( (b**2) - (4 * a * c) )
#         val += calc
#     except ValueError:
#         print("Discriminant has negative sqrt. ")
#         val = "None"

#     return val

# print(f"Positive root: {discrim(1)}; Negative root: {discrim(-1)}")

'''
Task 3
'''

# input should be in order of a, b, c
read: str = input("Input 3 numbers seperated by a space: ")
rawValues: list[str] = read.split(" ")
values: list[str] = []
[values.append(float(x)) for x in rawValues]

a,b,c = values

print(
    (
        max(a+b, c)!=c 
        and max(a+c,b)!=b 
        and max(c+b,a)!=a
    )
    and "Is a triangle" or "Not a triangle"
)

'''

'''