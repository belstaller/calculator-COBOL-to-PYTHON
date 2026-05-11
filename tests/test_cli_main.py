"""Tests for the Python CLI entry point wiring."""

import unittest
from unittest.mock import patch

from src.application.services import CalculatorSessionService
from src.interfaces.cli.console_handlers import ConsoleCalculatorInteraction
from src.interfaces.cli.main import create_calculator_application, main


class TestCliMain(unittest.TestCase):
    """Verify CLI runtime composition and exit behavior."""

    def test_create_calculator_application_composes_console_interaction_and_service(self):
        application = create_calculator_application()

        self.assertIsInstance(application, CalculatorSessionService)
        self.assertIsInstance(application._interaction, ConsoleCalculatorInteraction)

    def test_main_runs_application(self):
        with patch('src.interfaces.cli.main.create_calculator_application') as create_application:
            application = create_application.return_value

            exit_code = main()

            application.run.assert_called_once_with()
            self.assertEqual(exit_code, 0)

    def test_main_handles_keyboard_interrupt_as_clean_exit(self):
        with patch('src.interfaces.cli.main.create_calculator_application') as create_application:
            application = create_application.return_value
            application.run.side_effect = KeyboardInterrupt

            exit_code = main()

            application.run.assert_called_once_with()
            self.assertEqual(exit_code, 0)


if __name__ == '__main__':
    unittest.main()
