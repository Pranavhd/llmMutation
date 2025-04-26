# example.py

def divide(a, b):
    """This function divides the first number by the second."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b