import { CreateCalculationUseCase } from '@/src/application/use-cases/create-calculation-use-case';
import { ListCalculationsUseCase } from '@/src/application/use-cases/list-calculations-use-case';
import { InMemoryCalculationRepository } from '@/src/infrastructure/repositories/in-memory-calculation-repository';
import { RandomCalculationIdGenerator } from '@/src/infrastructure/services/random-calculation-id-generator';

const repository = new InMemoryCalculationRepository();
const idGenerator = new RandomCalculationIdGenerator();

export const calculationModule = {
  createCalculationUseCase: new CreateCalculationUseCase(repository, idGenerator),
  listCalculationsUseCase: new ListCalculationsUseCase(repository),
};
