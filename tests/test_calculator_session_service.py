"""Tests for calculator session orchestration service."""

import os
import sys
import unittest

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    def test_runs_single_successful_cycle_and_exits(self):
        interaction = FakeInteraction(
            requests=[CalculationRequest(left_operand=10, operator='+', right_operand=5)],
            continue_responses=[False],
        )

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(interaction.header_displayed, 1)
        self.assertEqual(interaction.errors, [])
        self.assertEqual(len(interaction.results), 1)
        self.assertEqual(
            interaction.results[0],
            CalculationResponse(left_operand=10, operator='+', right_operand=5, result=15),
        )
        self.assertEqual(interaction.request_continue_calls, 1)

    def test_repeats_until_continue_returns_false(self):
        interaction = FakeInteraction(
            requests=[
                CalculationRequest(left_operand=8, operator='*', right_operand=2),
                CalculationRequest(left_operand=20, operator='-', right_operand=3),
            ],
            continue_responses=[True, False],
        )

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(len(interaction.results), 2)
        self.assertEqual(interaction.results[0].result, 16)
        self.assertEqual(interaction.results[1].result, 17)
        self.assertEqual(interaction.request_continue_calls, 2)

    def test_invalid_operator_triggers_full_request_reentry(self):
        interaction = FakeInteraction(
            requests=[
                CalculationRequest(left_operand=10, operator='%', right_operand=5),
                CalculationRequest(left_operand=7, operator='+', right_operand=6),
            ],
            continue_responses=[False],
        )

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(interaction.errors, [INVALID_OPERATION_ERROR])
        self.assertEqual(interaction.request_calculation_calls, 2)
        self.assertEqual(len(interaction.results), 1)
        self.assertEqual(interaction.results[0].result, 13)

    def test_division_by_zero_triggers_full_request_reentry(self):
        interaction = FakeInteraction(
            requests=[
                CalculationRequest(left_operand=10, operator='/', right_operand=0),
                CalculationRequest(left_operand=10, operator='/', right_operand=2),
            ],
            continue_responses=[False],
        )

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(interaction.errors, [DIVISION_BY_ZERO_ERROR])
        self.assertEqual(interaction.request_calculation_calls, 2)
        self.assertEqual(len(interaction.results), 1)
        self.assertEqual(interaction.results[0].result, 5)

    def test_exit_signal_during_request_stops_session(self):
        interaction = FakeInteraction(requests=[None], continue_responses=[])

        service = CalculatorSessionService(interaction)
        service.run()

        self.assertEqual(interaction.header_displayed, 1)
        self.assertEqual(interaction.results, [])
        self.assertEqual(interaction.errors, [])
        self.assertEqual(interaction.request_continue_calls, 0)


if __name__ == '__main__':
    unittest.main()
