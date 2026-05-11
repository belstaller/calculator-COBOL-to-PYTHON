#!/usr/bin/env python3
"""Python CLI entry point for the calculator application."""

from __future__ import annotations

from src.application.services import CalculatorSessionService
from src.interfaces.cli.console_handlers import ConsoleCalculatorInteraction


def create_calculator_application() -> CalculatorSessionService:
    """Compose the calculator CLI runtime dependencies."""
    interaction = ConsoleCalculatorInteraction()
    return CalculatorSessionService(interaction)


def main() -> int:
    """Run the calculator application and translate normal interrupts into clean exits."""
    application = create_calculator_application()

    try:
        application.run()
    except KeyboardInterrupt:
        return 0

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
