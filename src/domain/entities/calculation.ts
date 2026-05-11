import { Operation } from '../value-objects/operation';

export class Calculation {
  public readonly id: string;
  public readonly leftOperand: number;
  public readonly rightOperand: number;
  public readonly operation: Operation;
  public readonly result: number;
  public readonly createdAt: Date;

  constructor(params: {
    id: string;
    leftOperand: number;
    rightOperand: number;
    operation: Operation;
    createdAt?: Date;
  }) {
    if (!params.id.trim()) {
      throw new Error('Calculation id is required.');
    }

    if (!Number.isFinite(params.leftOperand) || !Number.isFinite(params.rightOperand)) {
      throw new Error('Operands must be finite numbers.');
    }

    if (params.operation.equals(Operation.divide()) && params.rightOperand === 0) {
      throw new Error('Division by zero is not allowed.');
    }

    this.id = params.id;
    this.leftOperand = params.leftOperand;
    this.rightOperand = params.rightOperand;
    this.operation = params.operation;
    this.result = params.operation.apply(params.leftOperand, params.rightOperand);
    this.createdAt = params.createdAt ?? new Date();
  }
}
