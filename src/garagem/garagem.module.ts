import {  Module } from '@nestjs/common';
import { GaragemController } from './garagem.controller';
import { GaragemService } from './garagem.service';

@Module({
  controllers: [GaragemController],
  providers: [GaragemService]
})
export class GaragemModule {}
