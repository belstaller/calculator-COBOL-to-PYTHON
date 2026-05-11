"""Application service orchestrating a full calculator interaction session."""

from dataclasses import dataclass
from typing import Optional, Protocol, Union

from src.domain import Calculator


Number = Union[int, float]


@dataclass(frozen=True)
class CalculationRequest:
    """Input required to perform a calculator operation."""

    left_operand: Number
    operator: str
    right_operand: Number


@dataclass(frozen=True)
class CalculationResponse:
    """Calculated result ready for presentation."""

    left_operand: Number
    operator: str
    right_operand: Number
    result: float


class CalculatorSessionInteraction(Protocol):
    """Framework-agnostic interaction contract for calculator sessions."""

    def display_header(self) -> None:
        """Render the calculator header or welcome content."""

    def request_calculation(self) -> Optional[CalculationRequest]:
        """Collect one full calculation request or return None to exit."""

    def display_validation_error(self, message: str) -> None:
        """Present a validation error that requires full request re-entry."""

    def display_result(self, response: CalculationResponse) -> None:
        """Present a successful calculation result."""

    def request_continue(self) -> bool:
        """Return True to continue the session, False to exit."""


class CalculatorSessionService:
    """Coordinates one calculator session cycle using the domain calculator."""

    def __init__(self, interaction: CalculatorSessionInteraction) -> None:
        self._interaction = interaction

    def run(self) -> None:
        """Run calculator cycles until the interaction layer signals exit."""
        self._interaction.display_header()

        while True:
            request = self._collect_valid_request()
            if request is None:
                return

            result = Calculator.calculate(
                request.left_operand,
                request.right_operand,
                request.operator,
            )
            self._interaction.display_result(
                CalculationResponse(
                    left_operand=request.left_operand,
                    operator=request.operator,
                    right_operand=request.right_operand,
                    result=result,
                )
            )

            if not self._interaction.request_continue():
                return

    def _collect_valid_request(self) -> Optional[CalculationRequest]:
        """Collect a full calculation request, re-prompting on recoverable validation errors."""
        while True:
            request = self._interaction.request_calculation()
            if request is None:
                return None

            try:
                Calculator.validate_operation(request.operator)
                Calculator.validate_division_by_zero(request.operator, request.right_operand)
                return request
            except ValueError as error:
                self._interaction.display_validation_error(str(error))
