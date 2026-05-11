"""Operation value object representing calculator operations."""

from typing import Literal, Union


OperationType = Literal['+', '-', '*', '/']
Number = Union[int, float]
INVALID_OPERATION_ERROR = 'Invalid operation.'


class Operation:
    """
    Value object representing a calculator operation.

    Supports addition (+), subtraction (-), multiplication (*), and division (/).
    Immutable and validates operation type on construction.
    """

    def __init__(self, value: OperationType) -> None:
        """
        Create an Operation value object.

        Args:
            value: The operation symbol (+, -, *, /)

        Raises:
            ValueError: If the operation is not supported
        """
        if value not in ('+', '-', '*', '/'):
            raise ValueError(INVALID_OPERATION_ERROR)
        self._value = value

    @staticmethod
    def add() -> 'Operation':
        """Create an addition operation."""
        return Operation('+')

    @staticmethod
    def subtract() -> 'Operation':
        """Create a subtraction operation."""
        return Operation('-')

    @staticmethod
    def multiply() -> 'Operation':
        """Create a multiplication operation."""
        return Operation('*')

    @staticmethod
    def divide() -> 'Operation':
        """Create a division operation."""
        return Operation('/')

    @staticmethod
    def from_string(value: str) -> 'Operation':
        """
        Create an Operation from a string representation.

        Args:
            value: Operation symbol (+, -, *, /)

        Returns:
            Operation instance

        Raises:
            ValueError: If the operation is not supported
        """
        if value == '+':
            return Operation.add()
        if value == '-':
            return Operation.subtract()
        if value == '*':
            return Operation.multiply()
        if value == '/':
            return Operation.divide()
        raise ValueError(INVALID_OPERATION_ERROR)

    def apply(self, left: Number, right: Number) -> float:
        """
        Apply the operation to two operands.

        Args:
            left: Left operand
            right: Right operand

        Returns:
            The result of applying the operation
        """
        if self._value == '+':
            return left + right
        if self._value == '-':
            return left - right
        if self._value == '*':
            return left * right
        if self._value == '/':
            return left / right
        raise ValueError(INVALID_OPERATION_ERROR)

    def __eq__(self, other: object) -> bool:
        """Check equality with another Operation."""
        if not isinstance(other, Operation):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """Return hash for use in sets and dicts."""
        return hash(self._value)

    def __str__(self) -> str:
        """Return string representation of the operation."""
        return self._value

    def __repr__(self) -> str:
        """Return developer-friendly representation."""
        return f"Operation('{self._value}')"
