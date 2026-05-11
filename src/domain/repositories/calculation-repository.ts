import { Calculation } from '../entities/calculation';

export interface CalculationRepository {
  save(calculation: Calculation): Promise<void>;
  findAll(): Promise<Calculation[]>;
}
