The following prompt was used to generate unit tests:
Create some simple pytest unit tests for the following code: def main(): print("Simple Calculator") a = float(input("Enter first number: ")) operator = input("Enter operator (+, -, *, /): ") b = float(input("Enter second number: ")) if operator == "+": result = a + b elif operator == "-": result = a - b elif operator == "*": result = a * b elif operator == "/": if b == 0: print("Error: division by zero") return result = a / b else: print("Invalid operator") return print("Result:", result) if __name__ == "__main__": main()

Everything from def main() on is just the calculator.py code

It generated very standard tests. A test was created for each arithmetic portion of the function. One for addition, subtraction, multiplication, and division. It additionally created a test for a zero division error and using an improper operator to perform a simple calculation.