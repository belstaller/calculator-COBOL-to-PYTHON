"""
Tests for the Calculator domain module.

These tests verify that the business rules are correctly implemented:
- Addition, subtraction, multiplication, and division operations
- Invalid operator rejection
- Division by zero rejection
- Zero is valid for non-division operations
"""

import os
import sys
import unittest

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain import Calculator, Operation
from src.domain.services.calculator import (
    DIVISION_BY_ZERO_ERROR,
    INVALID_OPERATION_ERROR,
)


class TestOperation(unittest.TestCase):
    """Test the Operation value object."""

    def test_create_addition_operation(self):
        """Test creating an addition operation."""
        op = Operation.add()
        self.assertEqual(str(op), '+')

    def test_create_subtraction_operation(self):
        """Test creating a subtraction operation."""
        op = Operation.subtract()
        self.assertEqual(str(op), '-')

    def test_create_multiplication_operation(self):
        """Test creating a multiplication operation."""
        op = Operation.multiply()
        self.assertEqual(str(op), '*')

    def test_create_division_operation(self):
        """Test creating a division operation."""
        op = Operation.divide()
        self.assertEqual(str(op), '/')

    def test_from_string_addition(self):
        """Test creating operation from string '+'."""
        op = Operation.from_string('+')
        self.assertEqual(str(op), '+')

    def test_from_string_subtraction(self):
        """Test creating operation from string '-'."""
        op = Operation.from_string('-')
        self.assertEqual(str(op), '-')

    def test_from_string_multiplication(self):
        """Test creating operation from string '*'."""
        op = Operation.from_string('*')
        self.assertEqual(str(op), '*')

    def test_from_string_division(self):
        """Test creating operation from string '/'."""
        op = Operation.from_string('/')
        self.assertEqual(str(op), '/')

    def test_from_string_invalid_operator(self):
        """Test that invalid operator raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Operation.from_string('%')
        self.assertEqual(str(context.exception), INVALID_OPERATION_ERROR)

    def test_direct_construction_invalid(self):
        """Test that direct construction with invalid operator raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Operation('&')
        self.assertEqual(str(context.exception), INVALID_OPERATION_ERROR)

    def test_apply_addition(self):
        """Test applying addition operation."""
        op = Operation.add()
        result = op.apply(10, 5)
        self.assertEqual(result, 15)

    def test_apply_subtraction(self):
        """Test applying subtraction operation."""
        op = Operation.subtract()
        result = op.apply(10, 5)
        self.assertEqual(result, 5)

    def test_apply_multiplication(self):
        """Test applying multiplication operation."""
        op = Operation.multiply()
        result = op.apply(10, 5)
        self.assertEqual(result, 50)

    def test_apply_division(self):
        """Test applying division operation."""
        op = Operation.divide()
        result = op.apply(10, 5)
        self.assertEqual(result, 2)

    def test_operation_equality(self):
        """Test that operations with same value are equal."""
        op1 = Operation.add()
        op2 = Operation.from_string('+')
        self.assertEqual(op1, op2)

    def test_operation_inequality(self):
        """Test that operations with different values are not equal."""
        op1 = Operation.add()
        op2 = Operation.subtract()
        self.assertNotEqual(op1, op2)


class TestCalculator(unittest.TestCase):
    """Test the Calculator domain service."""

    def test_calculate_addition(self):
        """Test addition calculation."""
        result = Calculator.calculate(10, 5, '+')
        self.assertEqual(result, 15)

    def test_calculate_subtraction(self):
        """Test subtraction calculation."""
        result = Calculator.calculate(10, 5, '-')
        self.assertEqual(result, 5)

    def test_calculate_multiplication(self):
        """Test multiplication calculation."""
        result = Calculator.calculate(10, 5, '*')
        self.assertEqual(result, 50)

    def test_calculate_division(self):
        """Test division calculation."""
        result = Calculator.calculate(10, 5, '/')
        self.assertEqual(result, 2)

    def test_calculate_with_floats(self):
        """Test calculations with floating point numbers."""
        result = Calculator.calculate(10.5, 2.5, '+')
        self.assertEqual(result, 13.0)

    def test_calculate_with_negative_numbers(self):
        """Test calculations with negative numbers."""
        result = Calculator.calculate(-10, 5, '+')
        self.assertEqual(result, -5)

    def test_zero_as_left_operand_addition(self):
        """Test that zero is valid as left operand for addition."""
        result = Calculator.calculate(0, 5, '+')
        self.assertEqual(result, 5)

    def test_zero_as_right_operand_addition(self):
        """Test that zero is valid as right operand for addition."""
        result = Calculator.calculate(5, 0, '+')
        self.assertEqual(result, 5)

    def test_zero_as_left_operand_subtraction(self):
        """Test that zero is valid as left operand for subtraction."""
        result = Calculator.calculate(0, 5, '-')
        self.assertEqual(result, -5)

    def test_zero_as_right_operand_subtraction(self):
        """Test that zero is valid as right operand for subtraction."""
        result = Calculator.calculate(5, 0, '-')
        self.assertEqual(result, 5)

    def test_zero_as_left_operand_multiplication(self):
        """Test that zero is valid as left operand for multiplication."""
        result = Calculator.calculate(0, 5, '*')
        self.assertEqual(result, 0)

    def test_zero_as_right_operand_multiplication(self):
        """Test that zero is valid as right operand for multiplication."""
        result = Calculator.calculate(5, 0, '*')
        self.assertEqual(result, 0)

    def test_zero_as_left_operand_division(self):
        """Test that zero is valid as left operand (dividend) for division."""
        result = Calculator.calculate(0, 5, '/')
        self.assertEqual(result, 0)

    def test_division_by_zero_raises_error(self):
        """Test that division by zero raises ValueError with specific message."""
        with self.assertRaises(ValueError) as context:
            Calculator.calculate(10, 0, '/')
        self.assertEqual(str(context.exception), DIVISION_BY_ZERO_ERROR)

    def test_invalid_operator_raises_error(self):
        """Test that invalid operator raises standardized ValueError."""
        with self.assertRaises(ValueError) as context:
            Calculator.calculate(10, 5, '%')
        self.assertEqual(str(context.exception), INVALID_OPERATION_ERROR)

    def test_validate_operation_valid_operators(self):
        """Test that validate_operation accepts valid operators."""
        Calculator.validate_operation('+')
        Calculator.validate_operation('-')
        Calculator.validate_operation('*')
        Calculator.validate_operation('/')

    def test_validate_operation_invalid_operator(self):
        """Test that validate_operation rejects invalid operators."""
        with self.assertRaises(ValueError) as context:
            Calculator.validate_operation('%')
        self.assertEqual(str(context.exception), INVALID_OPERATION_ERROR)

    def test_validate_division_by_zero_catches_zero(self):
        """Test that validate_division_by_zero catches division by zero."""
        with self.assertRaises(ValueError) as context:
            Calculator.validate_division_by_zero('/', 0)
        self.assertEqual(str(context.exception), DIVISION_BY_ZERO_ERROR)

    def test_validate_division_by_zero_allows_nonzero(self):
        """Test that validate_division_by_zero allows non-zero divisor."""
        Calculator.validate_division_by_zero('/', 5)

    def test_validate_division_by_zero_allows_zero_for_other_operations(self):
        """Test that validate_division_by_zero allows zero for non-division operations."""
        Calculator.validate_division_by_zero('+', 0)
        Calculator.validate_division_by_zero('-', 0)
        Calculator.validate_division_by_zero('*', 0)


class TestCalculatorIntegration(unittest.TestCase):
    """Integration tests covering complete calculator workflows."""

    def test_multiple_calculations_sequence(self):
        """Test performing multiple calculations in sequence."""
        result1 = Calculator.calculate(100, 50, '+')
        result2 = Calculator.calculate(result1, 30, '-')
        result3 = Calculator.calculate(result2, 2, '*')
        result4 = Calculator.calculate(result3, 4, '/')

        self.assertEqual(result1, 150)
        self.assertEqual(result2, 120)
        self.assertEqual(result3, 240)
        self.assertEqual(result4, 60)

    def test_error_handling_does_not_affect_subsequent_calculations(self):
        """Test that error handling doesn't break subsequent valid calculations."""
        result1 = Calculator.calculate(10, 5, '+')
        self.assertEqual(result1, 15)

        with self.assertRaises(ValueError):
            Calculator.calculate(10, 0, '/')

        result3 = Calculator.calculate(20, 4, '/')
        self.assertEqual(result3, 5)


if __name__ == '__main__':
    unittest.main()
