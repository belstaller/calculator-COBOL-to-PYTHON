"""Tests for calculator session orchestration service."""

import unittest

from src.application.services.calculator_session_service import (
    CalculationRequest,
    CalculationResponse,
    CalculatorSessionService,
)
from src.domain.services.calculator import DIVISION_BY_ZERO_ERROR, INVALID_OPERATION_ERROR


class FakeInteraction:
    """Test double for the session interaction contract."""

    def __init__(self, requests, continue_responses):
        self._requests = list(requests)
        self._continue_responses = list(continue_responses)
        self.header_displayed = 0
        self.errors = []
        self.results = []
        self.request_calculation_calls = 0
        self.request_continue_calls = 0

    def display_header(self) -> None:
        self.header_displayed += 1

    def request_calculation(self):
        self.request_calculation_calls += 1
        if not self._requests:
            return None
        return self._requests.pop(0)

    def display_validation_error(self, message: str) -> None:
        self.errors.append(message)

    def display_result(self, response: CalculationResponse) -> None:
        self.results.append(response)

    def request_continue(self) -> bool:
        self.request_continue_calls += 1
        if not self._continue_responses:
            return False
        return self._continue_responses.pop(0)


class TestCalculatorSessionService(unittest.TestCase):
    """Test orchestration of the calculator interaction cycle."""

    def test_invalid_operator_triggers_reentry_of_full_calculation_flow(self):
        interaction = FakeInteraction(
            requests=[
                CalculationRequest(left_operand=10, operator='%', right_operand=5),
                CalculationRequest(left_operand=7, operator='+', right_operand=6),
            ],
            continue_responses=[False],
        )

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(interaction.header_displayed, 1)
        self.assertEqual(interaction.errors, [INVALID_OPERATION_ERROR])
        self.assertEqual(interaction.request_calculation_calls, 2)
        self.assertEqual(
            interaction.results,
            [
                CalculationResponse(
                    left_operand=7,
                    operator='+',
                    right_operand=6,
                    result=13,
                )
            ],
        )
        self.assertEqual(interaction.request_continue_calls, 1)

    def test_division_by_zero_triggers_reentry_of_full_calculation_flow(self):
        interaction = FakeInteraction(
            requests=[
                CalculationRequest(left_operand=10, operator='/', right_operand=0),
                CalculationRequest(left_operand=10, operator='/', right_operand=2),
            ],
            continue_responses=[False],
        )

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(interaction.header_displayed, 1)
        self.assertEqual(interaction.errors, [DIVISION_BY_ZERO_ERROR])
        self.assertEqual(interaction.request_calculation_calls, 2)
        self.assertEqual(
            interaction.results,
            [
                CalculationResponse(
                    left_operand=10,
                    operator='/',
                    right_operand=2,
                    result=5,
                )
            ],
        )
        self.assertEqual(interaction.request_continue_calls, 1)


if __name__ == '__main__':
    unittest.main()
