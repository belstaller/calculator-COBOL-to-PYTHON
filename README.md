# calculator migration full workflow test

Production-ready boilerplate that combines a Next.js interface with Python CLI support while following Clean Architecture.

## Stack
- Next.js 14
- React 18
- TypeScript
- Python 3

## Setup
1. Install Node.js 18+ and Python 3.10+.
2. Install JavaScript dependencies:
   ```bash
   npm install
   ```
3. Start the web app:
   ```bash
   npm run dev
   ```
4. Run the Python CLI calculator:
   ```bash
   python -m src.interfaces.cli.main
   ```
   Or use the npm convenience script:
   ```bash
   npm run python:run
   ```

## Available scripts
- `npm run dev` — start Next.js in development
- `npm run build` — build the production app
- `npm run start` — run the production server
- `npm run lint` — lint the project
- `npm run typecheck` — run TypeScript checks
- `npm run format` — format files with Prettier
- `npm run python:run` — run the Python CLI entry point
- `python -m src.interfaces.cli.main` — run the calculator natively with Python

## Clean Architecture layers
- `src/domain/` — entities, value objects, domain services, repository interfaces
- `src/application/` — use cases and DTOs that orchestrate domain behavior
- `src/infrastructure/` — repository implementations and external integrations
- `src/interfaces/` — HTTP routes, web UI adapters, and CLI entry points

## Example workflow
This scaffold includes a calculator migration example:
- A domain `Calculation` entity and `Operation` value object
- An application use case to create and list calculations
- An infrastructure in-memory repository implementation
- A Next.js route handler and UI page
- A Python CLI entry point for simple execution examples
