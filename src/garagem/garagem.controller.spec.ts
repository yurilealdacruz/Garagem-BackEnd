import { Test, TestingModule } from '@nestjs/testing';
import { GaragemController } from './garagem.controller';

describe('GaragemController', () => {
  let controller: GaragemController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [GaragemController],
    }).compile();

    controller = module.get<GaragemController>(GaragemController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
