import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Habilita CORS para todas as origens (dev)
  app.enableCors();

  await app.listen(3000);
}
bootstrap();
