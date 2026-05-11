'use client';

import type { ChangeEvent, FormEvent } from 'react';
import { useMemo, useState } from 'react';

type CalculationState = {
  expression: string;
  result: number;
};

const INVALID_OPERATION_ERROR = 'Invalid operation.';
const DIVISION_BY_ZERO_ERROR = 'Division by zero is not allowed.';
const DEFAULT_OPERATOR = '+';

function parseNumericValue(value: string): number {
  return Number(value);
}

function formatNumber(value: number): string {
  return Number.isInteger(value) ? value.toString() : value.toString();
}

function validateOperation(operator: string): void {
  if (!['+', '-', '*', '/'].includes(operator)) {
    throw new Error(INVALID_OPERATION_ERROR);
  }
}

function validateDivisionByZero(operator: string, rightOperand: number): void {
  if (operator === '/' && rightOperand === 0) {
    throw new Error(DIVISION_BY_ZERO_ERROR);
  }
}

function calculate(leftOperand: number, rightOperand: number, operator: string): number {
  validateOperation(operator);
  validateDivisionByZero(operator, rightOperand);

  switch (operator) {
    case '+':
      return leftOperand + rightOperand;
    case '-':
      return leftOperand - rightOperand;
    case '*':
      return leftOperand * rightOperand;
    case '/':
      return leftOperand / rightOperand;
    default:
      throw new Error(INVALID_OPERATION_ERROR);
  }
}

export default function HomePage() {
  const [leftOperand, setLeftOperand] = useState('10');
  const [operator, setOperator] = useState(DEFAULT_OPERATOR);
  const [rightOperand, setRightOperand] = useState('5');
  const [errorMessage, setErrorMessage] = useState('');
  const [calculation, setCalculation] = useState<CalculationState | null>(null);
  const [sessionEnded, setSessionEnded] = useState(false);

  const usageExample = useMemo(() => 'Example: 10 + 5', []);

  const handleCalculate = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSessionEnded(false);
    setErrorMessage('');
    setCalculation(null);

    const parsedLeftOperand = parseNumericValue(leftOperand);
    const parsedRightOperand = parseNumericValue(rightOperand);

    if (Number.isNaN(parsedLeftOperand) || Number.isNaN(parsedRightOperand)) {
      setErrorMessage('Enter valid numeric values for both numbers.');
      return;
    }

    try {
      const result = calculate(parsedLeftOperand, parsedRightOperand, operator.trim());
      setCalculation({
        expression: `${formatNumber(parsedLeftOperand)} ${operator.trim()} ${formatNumber(parsedRightOperand)}`,
        result,
      });
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'Unexpected error.');
    }
  };

  const handleReset = () => {
    setLeftOperand('10');
    setOperator(DEFAULT_OPERATOR);
    setRightOperand('5');
    setErrorMessage('');
    setCalculation(null);
    setSessionEnded(false);
  };

  const handleEndSession = () => {
    setSessionEnded(true);
    setCalculation(null);
    setErrorMessage('');
  };

  return (
    <main
      style={{
        fontFamily: 'sans-serif',
        padding: '2rem',
        maxWidth: '720px',
        margin: '0 auto',
        lineHeight: 1.5,
      }}
    >
      <h1>Calculator</h1>
      <p>Enter two numbers and choose an operator to perform a calculation.</p>

      <section
        style={{
          border: '1px solid #d0d7de',
          borderRadius: '8px',
          padding: '1rem',
          marginBottom: '1.5rem',
          backgroundColor: '#f6f8fa',
        }}
      >
        <h2 style={{ marginTop: 0 }}>Usage guidance</h2>
        <p>Supported operators: +, -, *, /</p>
        <p>{usageExample}</p>
        <p>Division by zero is not allowed.</p>
      </section>

      <form onSubmit={handleCalculate} style={{ display: 'grid', gap: '1rem' }}>
        <label style={{ display: 'grid', gap: '0.5rem' }}>
          <span>First value</span>
          <input
            type="number"
            inputMode="decimal"
            value={leftOperand}
            onChange={(event: ChangeEvent<HTMLInputElement>) => setLeftOperand(event.target.value)}
            step="any"
          />
        </label>

        <label style={{ display: 'grid', gap: '0.5rem' }}>
          <span>Operator</span>
          <input
            type="text"
            value={operator}
            onChange={(event: ChangeEvent<HTMLInputElement>) => setOperator(event.target.value)}
            maxLength={1}
            aria-describedby="operator-help"
          />
        </label>
        <small id="operator-help">Use one of: +, -, *, /</small>

        <label style={{ display: 'grid', gap: '0.5rem' }}>
          <span>Second value</span>
          <input
            type="number"
            inputMode="decimal"
            value={rightOperand}
            onChange={(event: ChangeEvent<HTMLInputElement>) => setRightOperand(event.target.value)}
            step="any"
          />
        </label>

        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button type="submit">Calculate</button>
          <button type="button" onClick={handleReset}>
            Reset
          </button>
          <button type="button" onClick={handleEndSession}>
            End session
          </button>
        </div>
      </form>

      {errorMessage ? (
        <section
          style={{
            marginTop: '1.5rem',
            padding: '1rem',
            borderRadius: '8px',
            backgroundColor: '#fff1f0',
            border: '1px solid #ffa39e',
          }}
        >
          <h2 style={{ marginTop: 0 }}>Validation feedback</h2>
          <p>{errorMessage}</p>
        </section>
      ) : null}

      {calculation ? (
        <section
          style={{
            marginTop: '1.5rem',
            padding: '1rem',
            borderRadius: '8px',
            backgroundColor: '#f6ffed',
            border: '1px solid #b7eb8f',
          }}
        >
          <h2 style={{ marginTop: 0 }}>Result</h2>
          <p>
            Expression: <strong>{calculation.expression}</strong>
          </p>
          <p>
            Value: <strong>{formatNumber(calculation.result)}</strong>
          </p>
        </section>
      ) : null}

      {sessionEnded ? (
        <section
          style={{
            marginTop: '1.5rem',
            padding: '1rem',
            borderRadius: '8px',
            backgroundColor: '#fafafa',
            border: '1px solid #d9d9d9',
          }}
        >
          <p>Calculator session ended. Use Reset to start another calculation.</p>
        </section>
      ) : null}
    </main>
  );
}
