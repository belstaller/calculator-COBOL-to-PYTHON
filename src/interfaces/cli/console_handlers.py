"""Console interface handlers for calculator prompts, guidance, and results."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Callable, Optional, TextIO

# Add project root to path when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.application.services import CalculationRequest, CalculationResponse


ESCAPE = '\x1b'
INVALID_OPERATOR_FEEDBACK = 'Invalid operation. Please use one of: +, -, *, /.'
DIVISION_BY_ZERO_FEEDBACK = 'Division by zero is not allowed. Please enter a non-zero second value for division.'
GENERIC_VALIDATION_FEEDBACK = 'Invalid input. Please re-enter the full calculation.'


@dataclass(frozen=True)
class ContinuePromptResult:
    """Outcome of the post-result continue prompt."""

    should_continue: bool
    should_exit: bool


class ConsoleCalculatorInteraction:
    """Console implementation of the calculator session interaction contract."""

    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        output: TextIO = sys.stdout,
    ) -> None:
        self._input = input_func
        self._output = output

    def display_header(self) -> None:
        self._write('=== Calculator ===')
        self._write('Enter calculations one step at a time.')
        self._write('Example: 10 + 5')
        self._write('Use Ctrl+C at any prompt to exit.')
        self._write('')

    def request_calculation(self) -> Optional[CalculationRequest]:
        left_operand = self._read_number('First value: ')
        if left_operand is None:
            return None

        operator = self._read_operator('Operator (+, -, *, /): ')
        if operator is None:
            return None

        right_operand = self._read_number('Second value: ')
        if right_operand is None:
            return None

        return CalculationRequest(
            left_operand=left_operand,
            operator=operator,
            right_operand=right_operand,
        )

    def display_validation_error(self, message: str) -> None:
        if message == 'Invalid operation.':
            self._write(INVALID_OPERATOR_FEEDBACK)
        elif message == 'Division by zero is not allowed.':
            self._write(DIVISION_BY_ZERO_FEEDBACK)
        else:
            self._write(f'{GENERIC_VALIDATION_FEEDBACK} {message}')

    def display_result(self, response: CalculationResponse) -> None:
        self._write('')
        self._write(f'{response.left_operand} {response.operator} {response.right_operand} = {response.result}')

    def request_continue(self) -> bool:
        result = self.prompt_continue()
        return result.should_continue and not result.should_exit

    def prompt_continue(self) -> ContinuePromptResult:
        answer = self._input('Press any key to continue, or Escape to exit: ')
        if answer == ESCAPE:
            return ContinuePromptResult(should_continue=False, should_exit=True)
        return ContinuePromptResult(should_continue=True, should_exit=False)

    def _read_number(self, prompt: str) -> Optional[float]:
        raw_value = self._input(prompt).strip()
        try:
            return float(raw_value)
        except ValueError:
            self._write('Invalid number. Please enter a numeric value.')
            return None

    def _read_operator(self, prompt: str) -> Optional[str]:
        return self._input(prompt).strip()

    def _write(self, message: str) -> None:
        print(message, file=self._output)
