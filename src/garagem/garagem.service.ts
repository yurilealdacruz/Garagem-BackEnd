import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';

@Injectable()
export class GaragemService {

    constructor(private prisma: PrismaService) {}

   async registrarEvento(tipo: 'entrada' | 'saida', garagemNome: string) {
  // Busca a garagem (ou cria se não existir)
  let garagem = await this.prisma.garagem.findUnique({
    where: { nome: garagemNome }
  });
  if (!garagem) {
    garagem = await this.prisma.garagem.create({
      data: { nome: garagemNome }
    });
  }

  const entradas = await this.prisma.evento.count({
    where: { tipo: 'entrada', garagemId: garagem.id }
  });
  const saidas = await this.prisma.evento.count({
    where: { tipo: 'saida', garagemId: garagem.id }
  });

  if (tipo === 'saida' && saidas >= entradas) {
    return {
      mensagem: `Erro: não há carros na garagem '${garagemNome}' para registrar uma saída.`,
      contagemAtual: entradas - saidas,
    };
  }

  await this.prisma.evento.create({
    data: { tipo, garagemId: garagem.id },
  });

  const contagemAtual = tipo === 'entrada'
    ? entradas + 1 - saidas
    : entradas - (saidas + 1);

  return {
    mensagem: `Evento '${tipo}' registrado na garagem '${garagemNome}'.`,
    contagemAtual,
  };
}



async obterContagem(garagemNome: string) {
  const garagem = await this.prisma.garagem.findUnique({
    where: { nome: garagemNome }
  });

  if (!garagem) {
    return { contagemAtual: 0 };
  }

  const entradas = await this.prisma.evento.count({
    where: { tipo: 'entrada', garagemId: garagem.id }
  });
  const saidas = await this.prisma.evento.count({
    where: { tipo: 'saida', garagemId: garagem.id }
  });

  return { contagemAtual: entradas - saidas };
}



async obterHistorico(garagemNome: string, data: string) {
  if (!garagemNome || !data) {
    return { mensagem: 'Parâmetros "garagem" e "data" são obrigatórios.' };
  }

  const [year, month, day] = data.split('-').map(Number);
  const inicioDia = new Date(year, month - 1, day, 0, 0, 0, 0);
  const fimDia = new Date(year, month - 1, day, 23, 59, 59, 999);

  const garagem = await this.prisma.garagem.findUnique({
    where: { nome: garagemNome },
  });

  if (!garagem) {
    return { mensagem: `Garagem "${garagemNome}" não encontrada.` };
  }

  const eventos = await this.prisma.evento.findMany({
    where: {
      garagemId: garagem.id,
      createdAt: {
        gte: inicioDia,
        lte: fimDia,
      },
    },
    orderBy: {
      createdAt: 'asc',
    },
    select: {
      tipo: true,
      createdAt: true,
    },
  });

  return eventos;
}





}
