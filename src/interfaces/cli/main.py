from dataclasses import dataclass


@dataclass(frozen=True)
class CalculationResult:
    left_operand: float
    right_operand: float
    operation: str
    result: float


class CalculatorCliService:
    def execute(self, left_operand: float, right_operand: float, operation: str) -> CalculationResult:
        if operation == 'add':
            result = left_operand + right_operand
        elif operation == 'subtract':
            result = left_operand - right_operand
        elif operation == 'multiply':
            result = left_operand * right_operand
        elif operation == 'divide':
            if right_operand == 0:
                raise ValueError('Division by zero is not allowed.')
            result = left_operand / right_operand
        else:
            raise ValueError(f'Unsupported operation: {operation}')

        return CalculationResult(
            left_operand=left_operand,
            right_operand=right_operand,
            operation=operation,
            result=result,
        )


if __name__ == '__main__':
    service = CalculatorCliService()
    calculation = service.execute(10, 5, 'divide')
    print(
        f'{calculation.left_operand} {calculation.operation} {calculation.right_operand} = {calculation.result}'
    )
