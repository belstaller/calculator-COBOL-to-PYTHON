"""Integration-style tests for the Python calculator CLI flow."""

import io
import unittest
from unittest.mock import patch

from src.interfaces.cli.main import main


class TestCliMain(unittest.TestCase):
    """Verify CLI behavior through mocked console input and output."""

    def test_main_runs_successful_calculation_cycle_then_exits_after_result_display(self):
        output = io.StringIO()
        inputs = iter(['10', '+', '5', '\x1b'])

        def fake_input(prompt: str) -> str:
            return next(inputs)

        with patch('src.interfaces.cli.console_handlers.sys.stdout', output):
            with patch('builtins.input', side_effect=fake_input):
                exit_code = main()

        rendered = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn('=== Calculator ===', rendered)
        self.assertIn('10.0 + 5.0 = 15.0', rendered)

    def test_main_exits_cleanly_when_user_interrupts_during_input(self):
        output = io.StringIO()

        with patch('src.interfaces.cli.console_handlers.sys.stdout', output):
            with patch('builtins.input', side_effect=KeyboardInterrupt):
                exit_code = main()

        rendered = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn('=== Calculator ===', rendered)
        self.assertNotIn(' = ', rendered)


if __name__ == '__main__':
    unittest.main()
