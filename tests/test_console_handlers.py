"""Tests for console calculator interface handlers."""

import io
import unittest

from src.application.services import CalculationResponse
from src.interfaces.cli.console_handlers import (
    DIVISION_BY_ZERO_FEEDBACK,
    ESCAPE,
    GENERIC_VALIDATION_FEEDBACK,
    INVALID_OPERATOR_FEEDBACK,
    ConsoleCalculatorInteraction,
)


class TestConsoleCalculatorInteraction(unittest.TestCase):
    """Verify console rendering and structured input behavior."""

    def test_display_header_renders_guidance_and_example(self):
        output = io.StringIO()
        interaction = ConsoleCalculatorInteraction(input_func=lambda prompt: '', output=output)

        interaction.display_header()

        rendered = output.getvalue()
        self.assertIn('=== Calculator ===', rendered)
        self.assertIn('Example: 10 + 5', rendered)
        self.assertIn('Use Ctrl+C at any prompt to exit.', rendered)

    def test_request_calculation_collects_three_prompts(self):
        responses = iter(['10', '+', '5'])
        prompts = []
        output = io.StringIO()

        def fake_input(prompt: str) -> str:
            prompts.append(prompt)
            return next(responses)

        interaction = ConsoleCalculatorInteraction(input_func=fake_input, output=output)

        request = interaction.request_calculation()

        self.assertIsNotNone(request)
        self.assertEqual(request.left_operand, 10.0)
        self.assertEqual(request.operator, '+')
        self.assertEqual(request.right_operand, 5.0)
        self.assertEqual(
            prompts,
            ['First value: ', 'Operator (+, -, *, /): ', 'Second value: '],
        )

    def test_display_validation_error_formats_invalid_operator_feedback(self):
        output = io.StringIO()
        interaction = ConsoleCalculatorInteraction(input_func=lambda prompt: '', output=output)

        interaction.display_validation_error('Invalid operation.')

        self.assertIn(INVALID_OPERATOR_FEEDBACK, output.getvalue())

    def test_display_validation_error_formats_division_by_zero_feedback(self):
        output = io.StringIO()
        interaction = ConsoleCalculatorInteraction(input_func=lambda prompt: '', output=output)

        interaction.display_validation_error('Division by zero is not allowed.')

        self.assertIn(DIVISION_BY_ZERO_FEEDBACK, output.getvalue())

    def test_display_validation_error_formats_generic_feedback(self):
        output = io.StringIO()
        interaction = ConsoleCalculatorInteraction(input_func=lambda prompt: '', output=output)

        interaction.display_validation_error('Unexpected issue.')

        self.assertIn(f'{GENERIC_VALIDATION_FEEDBACK} Unexpected issue.', output.getvalue())

    def test_display_result_shows_completed_expression_and_result(self):
        output = io.StringIO()
        interaction = ConsoleCalculatorInteraction(input_func=lambda prompt: '', output=output)

        interaction.display_result(
            CalculationResponse(left_operand=10, operator='+', right_operand=5, result=15)
        )

        self.assertIn('10 + 5 = 15', output.getvalue())

    def test_prompt_continue_returns_exit_signal_for_escape(self):
        interaction = ConsoleCalculatorInteraction(
            input_func=lambda prompt: ESCAPE,
            output=io.StringIO(),
        )

        result = interaction.prompt_continue()

        self.assertFalse(result.should_continue)
        self.assertTrue(result.should_exit)
        self.assertFalse(interaction.request_continue())

    def test_prompt_continue_continues_for_non_escape_input(self):
        interaction = ConsoleCalculatorInteraction(
            input_func=lambda prompt: 'x',
            output=io.StringIO(),
        )

        result = interaction.prompt_continue()

        self.assertTrue(result.should_continue)
        self.assertFalse(result.should_exit)
        self.assertTrue(interaction.request_continue())


if __name__ == '__main__':
    unittest.main()
