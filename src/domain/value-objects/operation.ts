export class Operation {
  private constructor(private readonly value: 'add' | 'subtract' | 'multiply' | 'divide') {}

  static add(): Operation {
    return new Operation('add');
  }

  static subtract(): Operation {
    return new Operation('subtract');
  }

  static multiply(): Operation {
    return new Operation('multiply');
  }

  static divide(): Operation {
    return new Operation('divide');
  }

  static fromString(value: string): Operation {
    switch (value) {
      case 'add':
        return Operation.add();
      case 'subtract':
        return Operation.subtract();
      case 'multiply':
        return Operation.multiply();
      case 'divide':
        return Operation.divide();
      default:
        throw new Error(`Unsupported operation: ${value}`);
    }
  }

  equals(other: Operation): boolean {
    return this.value === other.value;
  }

  apply(left: number, right: number): number {
    switch (this.value) {
      case 'add':
        return left + right;
      case 'subtract':
        return left - right;
      case 'multiply':
        return left * right;
      case 'divide':
        return left / right;
    }
  }

  toString(): string {
    return this.value;
  }
}
