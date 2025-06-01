import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { GaragemService } from './garagem.service';

@Controller('garagem')
export class GaragemController {
  constructor(private readonly garagemService: GaragemService) {}

  @Post('evento')
  async registrarEvento(@Body() body: { evento: 'entrada' | 'saida'; garagem: string }) {
    return this.garagemService.registrarEvento(body.evento, body.garagem);
  }

  @Get('contagem')
  async obterContagem(@Query('garagem') garagem: string) {
    return this.garagemService.obterContagem(garagem);
  }

  @Get('historico')
  async obterHistorico(
    @Query('garagem') garagem: string,
    @Query('data') data: string,
) {
   return this.garagemService.obterHistorico(garagem, data);
}

}
