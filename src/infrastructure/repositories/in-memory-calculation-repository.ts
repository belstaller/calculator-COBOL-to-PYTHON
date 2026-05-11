import { Calculation } from '@/src/domain/entities/calculation';
import { CalculationRepository } from '@/src/domain/repositories/calculation-repository';

export class InMemoryCalculationRepository implements CalculationRepository {
  private readonly calculations: Calculation[] = [];

  async save(calculation: Calculation): Promise<void> {
    this.calculations.push(calculation);
  }

  async findAll(): Promise<Calculation[]> {
    return [...this.calculations];
  }
}
