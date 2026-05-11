import { CalculationViewDto } from '../dto/create-calculation.dto';
import { CalculationRepository } from '@/src/domain/repositories/calculation-repository';

export class ListCalculationsUseCase {
  constructor(private readonly repository: CalculationRepository) {}

  async execute(): Promise<CalculationViewDto[]> {
    const calculations = await this.repository.findAll();

    return calculations.map((calculation) => ({
      id: calculation.id,
      leftOperand: calculation.leftOperand,
      rightOperand: calculation.rightOperand,
      operation: calculation.operation.toString(),
      result: calculation.result,
      createdAt: calculation.createdAt.toISOString(),
    }));
  }
}
