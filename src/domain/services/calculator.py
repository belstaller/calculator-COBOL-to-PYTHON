"""Calculator domain service containing arithmetic and validation business rules."""

from typing import Union

from ..value_objects.operation import Operation


Number = Union[int, float]
INVALID_OPERATION_ERROR = 'Invalid operation.'
DIVISION_BY_ZERO_ERROR = 'Division by zero is not allowed.'


class Calculator:
    """
    Domain service that encapsulates calculator business rules.

    Provides validation and calculation logic for arithmetic operations.
    Independent from terminal or web concerns - can be reused by CLI and API layers.
    """

    @staticmethod
    def validate_operation(operator: str) -> None:
        """
        Validate that the operator is supported.

        Args:
            operator: The operation symbol to validate

        Raises:
            ValueError: If the operator is not one of +, -, *, /
        """
        if operator not in ('+', '-', '*', '/'):
            raise ValueError(INVALID_OPERATION_ERROR)

    @staticmethod
    def validate_division_by_zero(operator: str, right_operand: Number) -> None:
        """
        Validate that division by zero is not attempted.

        Args:
            operator: The operation symbol
            right_operand: The right operand (divisor)

        Raises:
            ValueError: If attempting division by exactly zero
        """
        if operator == '/' and right_operand == 0:
            raise ValueError(DIVISION_BY_ZERO_ERROR)

    @staticmethod
    def calculate(left_operand: Number, right_operand: Number, operator: str) -> float:
        """
        Perform a calculation with validation.

        Args:
            left_operand: First numeric operand
            right_operand: Second numeric operand
            operator: Operation symbol (+, -, *, /)

        Returns:
            The computed result

        Raises:
            ValueError: If the operator is not supported or division by zero is attempted
        """
        Calculator.validate_operation(operator)
        Calculator.validate_division_by_zero(operator, right_operand)

        operation = Operation.from_string(operator)
        return operation.apply(left_operand, right_operand)
