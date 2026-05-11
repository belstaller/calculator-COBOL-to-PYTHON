import { randomUUID } from 'crypto';
import { CalculationIdGenerator } from '@/src/domain/services/calculation-id-generator';

export class RandomCalculationIdGenerator implements CalculationIdGenerator {
  generate(): string {
    return randomUUID();
  }
}
