import { CreateCalculationDto, CalculationViewDto } from '../dto/create-calculation.dto';
import { Calculation } from '@/src/domain/entities/calculation';
import { CalculationRepository } from '@/src/domain/repositories/calculation-repository';
import { CalculationIdGenerator } from '@/src/domain/services/calculation-id-generator';
import { Operation } from '@/src/domain/value-objects/operation';

export class CreateCalculationUseCase {
  constructor(
    private readonly repository: CalculationRepository,
    private readonly idGenerator: CalculationIdGenerator,
  ) {}

  async execute(dto: CreateCalculationDto): Promise<CalculationViewDto> {
    const calculation = new Calculation({
      id: this.idGenerator.generate(),
      leftOperand: dto.leftOperand,
      rightOperand: dto.rightOperand,
      operation: Operation.fromString(dto.operation),
    });

    await this.repository.save(calculation);

    return {
      id: calculation.id,
      leftOperand: calculation.leftOperand,
      rightOperand: calculation.rightOperand,
      operation: calculation.operation.toString(),
      result: calculation.result,
      createdAt: calculation.createdAt.toISOString(),
    };
  }
}
