import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Habilita CORS para todas as origens (dev)
  app.enableCors();

  const port = process.env.PORT || 3000;  // Usa a porta do Render, ou 3000 localmente
  await app.listen(port);
  console.log(`Servidor rodando na porta ${port}`);
}
bootstrap();
