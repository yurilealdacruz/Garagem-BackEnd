import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { GaragemModule } from './garagem/garagem.module';
import { PrismaModule } from './prisma/prisma.module';
import { AppService } from './app.service';

@Module({
  imports: [GaragemModule, PrismaModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
