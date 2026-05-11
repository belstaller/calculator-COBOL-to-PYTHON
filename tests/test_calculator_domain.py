"""Tests for calculator business rules in the native Python domain module."""

import unittest

from src.domain import Calculator
from src.domain.services.calculator import (
    DIVISION_BY_ZERO_ERROR,
    INVALID_OPERATION_ERROR,
)


class TestCalculatorDomain(unittest.TestCase):
    """Verify arithmetic and validation semantics for the Python calculator."""

    def test_calculate_addition(self):
        self.assertEqual(Calculator.calculate(10, 5, '+'), 15)

    def test_calculate_subtraction(self):
        self.assertEqual(Calculator.calculate(10, 5, '-'), 5)

    def test_calculate_multiplication(self):
        self.assertEqual(Calculator.calculate(10, 5, '*'), 50)

    def test_calculate_division(self):
        self.assertEqual(Calculator.calculate(10, 5, '/'), 2)

    def test_invalid_operator_is_rejected_with_generic_validation_error(self):
        with self.assertRaises(ValueError) as context:
            Calculator.calculate(10, 5, '%')

        self.assertEqual(str(context.exception), INVALID_OPERATION_ERROR)

    def test_division_by_zero_is_rejected_with_explicit_user_facing_error(self):
        with self.assertRaises(ValueError) as context:
            Calculator.calculate(10, 0, '/')

        self.assertEqual(str(context.exception), DIVISION_BY_ZERO_ERROR)


if __name__ == '__main__':
    unittest.main()
