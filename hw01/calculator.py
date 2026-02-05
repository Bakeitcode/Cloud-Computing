def main():
    print("Simple Calculator")

    a = float(input("Enter first number: "))
    operator = input("Enter operator (+, -, *, /): ")
    b = float(input("Enter second number: "))

    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    elif operator == "/":
        if b == 0:
            print("Error: division by zero")
            return
        result = a / b
    else:
        print("Invalid operator")
        return

    print("Result:", result)


if __name__ == "__main__":
    main()
