"""CLI adapter for the framework-agnostic calculator session service."""

import os
import sys
from typing import Optional

# Add project root to path when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.application.services import (  # noqa: E402
    CalculationRequest,
    CalculationResponse,
    CalculatorSessionService,
)


class ConsoleCalculatorInteraction:
    """Console implementation of the calculator session interaction contract."""

    def display_header(self) -> None:
        print('=== Calculator ===')
        print("Enter 'q' at any prompt to exit.")

    def request_calculation(self) -> Optional[CalculationRequest]:
        left_operand = self._read_number('First number: ')
        if left_operand is None:
            return None

        operator = self._read_operator('Operator (+, -, *, /): ')
        if operator is None:
            return None

        right_operand = self._read_number('Second number: ')
        if right_operand is None:
            return None

        return CalculationRequest(
            left_operand=left_operand,
            operator=operator,
            right_operand=right_operand,
        )

    def display_validation_error(self, message: str) -> None:
        print(message)
        print('Please re-enter the full calculation.')

    def display_result(self, response: CalculationResponse) -> None:
        print(
            f'{response.left_operand} {response.operator} '
            f'{response.right_operand} = {response.result}'
        )

    def request_continue(self) -> bool:
        answer = input('Perform another calculation? (y/n): ').strip().lower()
        return answer in ('y', 'yes')

    def _read_number(self, prompt: str) -> Optional[float]:
        while True:
            raw_value = input(prompt).strip()
            if raw_value.lower() == 'q':
                return None

            try:
                return float(raw_value)
            except ValueError:
                print('Invalid number. Please try again.')

    def _read_operator(self, prompt: str) -> Optional[str]:
        raw_value = input(prompt).strip()
        if raw_value.lower() == 'q':
            return None
        return raw_value


if __name__ == '__main__':
    CalculatorSessionService(ConsoleCalculatorInteraction()).run()
