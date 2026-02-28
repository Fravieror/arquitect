a, b = 10,3
print(f"a = {a}, b = {b}") # f-string is a way to format strings in Python, 
# it allows you to embed expressions inside string literals, 
# using curly braces {}.
print(f"a+b = {a+b}")
print(f"a-b = {a-b}")
print(f"a*b = {a*b}")
print(f"a/b = {a/b}")
print(f"a // b = {a//b}") # // is floor division, it returns the integer part of the division
print(f"a%b = {a%b}")
print(f"a**b = {a**b}")
print(f"divmod(a,b) = {divmod(a,b)}") # divmod returns a tuple of (a//b, a%b), 
# what is a tuple? it's an immutable list, it cannot be changed after it's created, 
# it is defined by parentheses () instead of square brackets []

x = 5
x += 1
print(f"\nx += 1: {x}")

# chained comparisons (python-specific)
x = 15
print(f"10 < x < 20: {10 < x < 20}")
print(f"10 < x < 20: {10 < x < 20 < 30}")

# TERNARY OPERATOR
print("\n-- Ternary Operator --")
age = 17
status = "adult" if age >= 18 else "child"
print(f"{age}: is {status}")

# look into strings
text = "Hello, world!"
print(f"'world in text: {'world' in text}'")
