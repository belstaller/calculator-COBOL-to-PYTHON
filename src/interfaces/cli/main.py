"""CLI adapter entry point for the calculator session service."""

import os
import sys

# Add project root to path when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.application.services import CalculatorSessionService  # noqa: E402
from src.interfaces.cli.console_handlers import ConsoleCalculatorInteraction  # noqa: E402


if __name__ == '__main__':
    CalculatorSessionService(ConsoleCalculatorInteraction()).run()
