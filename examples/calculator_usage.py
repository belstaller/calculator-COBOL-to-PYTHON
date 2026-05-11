#!/usr/bin/env python3
"""
Demonstration of Python calculator domain module usage.

This script shows how to use the Calculator domain service and Operation value object
from different contexts (CLI, API, testing, etc.).
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain import Calculator, Operation


def demonstrate_basic_operations():
    """Demonstrate the four basic arithmetic operations."""
    print("=== Basic Operations ===\n")
    
    # Addition
    result = Calculator.calculate(10, 5, '+')
    print(f"10 + 5 = {result}")
    
    # Subtraction
    result = Calculator.calculate(10, 5, '-')
    print(f"10 - 5 = {result}")
    
    # Multiplication
    result = Calculator.calculate(10, 5, '*')
    print(f"10 * 5 = {result}")
    
    # Division
    result = Calculator.calculate(10, 5, '/')
    print(f"10 / 5 = {result}")
    print()


def demonstrate_operation_value_object():
    """Demonstrate using the Operation value object directly."""
    print("=== Operation Value Object ===\n")
    
    # Create operations using factory methods
    add_op = Operation.add()
    print(f"Created operation: {add_op}")
    
    # Create from string
    div_op = Operation.from_string('/')
    print(f"Created from string '/': {div_op}")
    
    # Apply operations
    result = add_op.apply(15, 3)
    print(f"Apply addition to 15 and 3: {result}")
    
    result = div_op.apply(15, 3)
    print(f"Apply division to 15 and 3: {result}")
    
    # Check equality
    another_add = Operation.from_string('+')
    print(f"Operations equal: {add_op == another_add}")
    print()


def demonstrate_zero_handling():
    """Demonstrate that zero is valid for non-division operations."""
    print("=== Zero Handling ===\n")
    
    # Zero as left operand
    result = Calculator.calculate(0, 5, '+')
    print(f"0 + 5 = {result}")
    
    # Zero as right operand
    result = Calculator.calculate(5, 0, '+')
    print(f"5 + 0 = {result}")
    
    # Zero in multiplication
    result = Calculator.calculate(5, 0, '*')
    print(f"5 * 0 = {result}")
    
    # Zero as dividend (numerator) - valid
    result = Calculator.calculate(0, 5, '/')
    print(f"0 / 5 = {result}")
    print()


def demonstrate_error_handling():
    """Demonstrate error handling for invalid operations and division by zero."""
    print("=== Error Handling ===\n")
    
    # Invalid operator
    try:
        Calculator.calculate(10, 5, '%')
    except ValueError as e:
        print(f"Invalid operator error: {e}")
    
    try:
        Calculator.calculate(10, 5, '^')
    except ValueError as e:
        print(f"Invalid operator error: {e}")
    
    # Division by zero
    try:
        Calculator.calculate(10, 0, '/')
    except ValueError as e:
        print(f"Division by zero error: {e}")
    
    # Using Operation directly with invalid operator
    try:
        Operation.from_string('&')
    except ValueError as e:
        print(f"Invalid operation construction: {e}")
    print()


def demonstrate_validation_methods():
    """Demonstrate using validation methods separately."""
    print("=== Validation Methods ===\n")
    
    # Validate operator
    try:
        Calculator.validate_operation('+')
        print("✓ '+' is a valid operator")
    except ValueError:
        print("✗ '+' is invalid")
    
    try:
        Calculator.validate_operation('%')
        print("✓ '%' is a valid operator")
    except ValueError as e:
        print(f"✗ '%' is invalid: {e}")
    
    # Validate division by zero
    try:
        Calculator.validate_division_by_zero('/', 5)
        print("✓ Division by 5 is valid")
    except ValueError:
        print("✗ Division by 5 is invalid")
    
    try:
        Calculator.validate_division_by_zero('/', 0)
        print("✓ Division by 0 is valid")
    except ValueError as e:
        print(f"✗ Division by 0 is invalid: {e}")
    
    # Zero is OK for other operations
    try:
        Calculator.validate_division_by_zero('+', 0)
        print("✓ Zero is valid for addition")
    except ValueError:
        print("✗ Zero is invalid for addition")
    print()


def demonstrate_float_support():
    """Demonstrate support for floating-point numbers."""
    print("=== Floating-Point Support ===\n")
    
    result = Calculator.calculate(10.5, 2.5, '+')
    print(f"10.5 + 2.5 = {result}")
    
    result = Calculator.calculate(7.5, 1.5, '-')
    print(f"7.5 - 1.5 = {result}")
    
    result = Calculator.calculate(3.5, 2.0, '*')
    print(f"3.5 * 2.0 = {result}")
    
    result = Calculator.calculate(9.0, 4.0, '/')
    print(f"9.0 / 4.0 = {result}")
    print()


def demonstrate_negative_numbers():
    """Demonstrate support for negative numbers."""
    print("=== Negative Numbers ===\n")
    
    result = Calculator.calculate(-10, 5, '+')
    print(f"-10 + 5 = {result}")
    
    result = Calculator.calculate(10, -5, '-')
    print(f"10 - (-5) = {result}")
    
    result = Calculator.calculate(-10, -5, '*')
    print(f"(-10) * (-5) = {result}")
    
    result = Calculator.calculate(-10, 2, '/')
    print(f"-10 / 2 = {result}")
    print()


def demonstrate_reusability():
    """Demonstrate how the domain logic can be reused in different contexts."""
    print("=== Reusability Example ===\n")
    
    # Simulating CLI usage
    def cli_calculator(left, right, op):
        """CLI wrapper around domain calculator."""
        try:
            result = Calculator.calculate(left, right, op)
            return f"Result: {result}"
        except ValueError as e:
            return f"Error: {e}"
    
    # Simulating API usage
    def api_calculator(left, right, op):
        """API wrapper around domain calculator."""
        try:
            result = Calculator.calculate(left, right, op)
            return {"success": True, "result": result}
        except ValueError as e:
            return {"success": False, "error": str(e)}
    
    # Both use the same domain logic
    print("CLI context:", cli_calculator(10, 5, '+'))
    print("API context:", api_calculator(10, 5, '+'))
    
    print("\nCLI error:", cli_calculator(10, 0, '/'))
    print("API error:", api_calculator(10, 0, '/'))
    print()


if __name__ == '__main__':
    print("Python Calculator Domain Module Demonstration")
    print("=" * 60)
    print()
    
    demonstrate_basic_operations()
    demonstrate_operation_value_object()
    demonstrate_zero_handling()
    demonstrate_error_handling()
    demonstrate_validation_methods()
    demonstrate_float_support()
    demonstrate_negative_numbers()
    demonstrate_reusability()
    
    print("=" * 60)
    print("Demonstration complete!")
