export interface CreateCalculationDto {
  leftOperand: number;
  rightOperand: number;
  operation: 'add' | 'subtract' | 'multiply' | 'divide';
}

export interface CalculationViewDto {
  id: string;
  leftOperand: number;
  rightOperand: number;
  operation: string;
  result: number;
  createdAt: string;
}
