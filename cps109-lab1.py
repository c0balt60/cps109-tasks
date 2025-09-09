from math import sqrt

'''
Task 1
> Convert celcius to farenheit / kelvin
'''

print("~ Task 1 ~")
read: str = input("Input Celcius: ")
celcius: float = float(read)

try:
    f: float = celcius * (9/5) + 32
    k: float = celcius + 273.15
    print(f"Farenheit: {round(f, 2)}; Kelvin: {round(k, 2)}")

except TypeError:
    print("Type conversion warning")


'''
Task 2
> Determine roots using quadratic formula
'''

print("\n~ Task 2 ~")
# input should be in order of a, b, c
read: str = input("Input 3 numbers seperated by a space: ")
rawValues: list[str] = read.split(" ")
values: list[float] = []
[values.append(float(x)) for x in rawValues]

divisor: float = 2 * (values[0])

# Discriminator calculation (+)
a, b, c = values
def discrim(sign: int) -> float | str:
    val: float|str = (sign * values[1])
    try:
        calc: float = sqrt( (b**2) - (4 * a * c) )
        val += calc
        round(val, 2)

    except ValueError:
        print("Discriminant has negative sqrt. ")
        val = "None"

    return val

print(f"Positive root: {discrim(1)}; Negative root: {discrim(-1)}")


'''
Task 3
> Determine if triangle is possible off of inputs
'''

print("\n~ Task 3 ~")
# input should be in order of a, b, c
read: str = input("Input 3 numbers seperated by a space: ")
rawValues: list[str] = read.split(" ")
values: list[float] = []
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
Task 4
> Calculate pentagon area
'''

print("\n~ Task 4 ~")
read: str = input("Input pentagon side length: ")
length: float = float(read)

area: float = .25 * sqrt( 5 * (5 + 2*sqrt(5))) * length**2

print(f"Pentagon with side length of {length} has area of {round(area, 2)}")


'''
Task 5
> Find nth fibonacci number
'''

print("\n~ Task 5 ~")
read: str = input("Enter fibonacci sequence number: ")
fibNum: int = int(read)

gr: float = (sqrt(5) + 1) * 0.5

# Fibonacci sequence
def fib(n: int):
    return ((2 + gr) * .2) * gr**n + ((3 - gr) * .2) * gr**-n

print(round(fib(fibNum), 2))
