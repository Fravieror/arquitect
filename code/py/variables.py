name = "John"
age = 30
salary = 75000.50
is_employed = True
grade = 'A'

PI = 3.14159
COMPANY = "TechCorp"

name_typed: str = "Jane"
age_typed: int = 25
salary_typed: float = 65000.00
is_active: bool = False

x,y,z = 1,2,3
a =b =c = 0 # all equal to 0

nullable_value = None

dynamic_var = 10
print(f"dynamic_var is {type(dynamic_var)}: {dynamic_var}")

dynamic_var = "Hello"
print(f"dynamic_var is {type(dynamic_var)}: {dynamic_var}")

dynamic_var = [1,2,3]
print(f"dynamic_var is {type(dynamic_var)}: {dynamic_var}")


# Print all variables
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Salary: {salary}")
print(f"Employed: {is_employed}")
print(f"PI: {PI}")
print(f"x, y, z: {x}, {y}, {z}")
print(f"Nullable: {nullable_value}")

# Check types
print(f"\nType checking:")
print(f"name type: {type(name)}")
print(f"age type: {type(age)}")
print(f"salary type: {type(salary)}")
print(f"is_employed type: {type(is_employed)}")

