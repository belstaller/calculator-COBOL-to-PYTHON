# Python Domain Layer - Calculator Business Rules

This directory contains the Python implementation of calculator business rules, ported from the COBOL calculator behavior. The domain layer is independent of CLI, web, or any external framework concerns.

## Architecture

The domain layer follows Clean Architecture principles:
- **No dependencies on external frameworks** - Pure Python only
- **No I/O operations** - No `input()` or `print()` calls
- **Reusable by any interface** - Can be called from CLI, web API, or any other layer

## Components

### Value Objects

#### `operation.py` - Operation Value Object

Represents a calculator operation (`+`, `-`, `*`, `/`).

**Key Features:**
- Immutable value object
- Validates operator on construction
- Factory methods for each operation type
- String conversion support
- Applies arithmetic operations to operands

**Usage:**
```python
from src.domain import Operation

op = Operation.add()
op = Operation.from_string('+')
result = op.apply(10, 5)
```

**Validation:**
- Rejects any operator not in `+`, `-`, `*`, `/`
- Raises `ValueError` with standardized message: `Invalid operation.`

### Domain Services

#### `calculator.py` - Calculator Domain Service

Encapsulates calculator business rules including validation and computation.

**Key Features:**
- Validates operators before computation
- Enforces division-by-zero business rule
- Performs arithmetic calculations
- Stateless service with static methods

**Usage:**
```python
from src.domain import Calculator

result = Calculator.calculate(10, 5, '+')
Calculator.validate_operation('+')
Calculator.validate_division_by_zero('/', 5)
```

## Business Rules

### Supported Operations

The calculator supports exactly four operations:
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`

### Invalid Operator Handling

Any unsupported operator raises a generic standardized error:

```python
ValueError('Invalid operation.')
```

This preserves the generic invalid-operator error path from the source behavior.

### Division by Zero

Division with a right operand of exactly `0` is rejected with a specific business-rule error:

```python
ValueError('Division by zero is not allowed.')
```

Zero remains valid for non-division operations, including when it appears as either operand.

### Numeric Support

The domain API accepts integers and floating-point numbers.

## Interface Independence

The domain layer has no direct terminal or web concerns:
- No `input()` calls
- No `print()` calls
- No framework coupling
- No runtime dependency on COBOL, GnuCOBOL, Make, or Git

This allows reuse from a Python CLI entry point today and future API integrations later.

## Testing

Tests for the domain behavior are located in `tests/test_calculator_domain.py`.
