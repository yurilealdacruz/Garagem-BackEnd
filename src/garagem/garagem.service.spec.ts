import { Test, TestingModule } from '@nestjs/testing';
import { GaragemService } from './garagem.service';

describe('GaragemService', () => {
  let service: GaragemService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [GaragemService],
    }).compile();

    service = module.get<GaragemService>(GaragemService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
