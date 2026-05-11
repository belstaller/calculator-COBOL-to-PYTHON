import { CreateCalculationDto } from '@/src/application/dto/create-calculation.dto';
import { calculationModule } from '../composition/calculation-module';

export class CalculationController {
  async create(input: CreateCalculationDto) {
    return calculationModule.createCalculationUseCase.execute(input);
  }

  async list() {
    return calculationModule.listCalculationsUseCase.execute();
  }
}

export const calculationController = new CalculationController();
