from django.shortcuts import render
from django.http import JsonResponse
from .models import CarAction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime
import pytz
import json

# === Configurações ===
FUSO_BRASIL = pytz.timezone('America/Sao_Paulo')


GARAGENS_VALIDAS = ['A', 'B']

GARAGE_LABELS = {
    'A': 'Garagem VIP',
    'B': 'Garagem CIMATEC PARK'
}

# === Views ===

def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods(["POST"])
def entrada(request, garage):
    if garage not in GARAGENS_VALIDAS:
        return JsonResponse({'error': 'Garagem inválida.'}, status=400)

    CarAction.objects.create(action='entrada', garage=garage)
    return JsonResponse({'message': f'Entrada registrada na Garagem {garage} com sucesso!'})


@csrf_exempt
@require_http_methods(["POST"])
def saida(request, garage):
    if garage not in GARAGENS_VALIDAS:
        return JsonResponse({'error': 'Garagem inválida.'}, status=400)

    entradas = CarAction.objects.filter(action='entrada', garage=garage).count()
    saidas = CarAction.objects.filter(action='saida', garage=garage).count()

    if entradas > saidas:
        CarAction.objects.create(action='saida', garage=garage)
        return JsonResponse({'message': f'Saída registrada na Garagem {garage} com sucesso!'})
    else:
        return JsonResponse({'error': f'Não há carros suficientes na Garagem {garage} para saída.'}, status=400)


def carros_na_garagem(request, garage):
    if garage not in GARAGENS_VALIDAS:
        return JsonResponse({'error': 'Garagem inválida.'}, status=400)

    entradas = CarAction.objects.filter(action='entrada', garage=garage).count()
    saidas = CarAction.objects.filter(action='saida', garage=garage).count()
    saldo = entradas - saidas

    return JsonResponse({'carros_na_garagem': saldo})


@csrf_exempt
@require_http_methods(["POST"])
def limpar_dados(request):
    CarAction.objects.all().delete()
    return JsonResponse({'message': 'Todos os registros foram apagados com sucesso!'})


@csrf_exempt
def historico_por_data(request, garagem, data_str):
    if garagem not in GARAGENS_VALIDAS:
        return JsonResponse({'error': 'Garagem inválida.'}, status=400)

    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        acoes = CarAction.objects.filter(
            garage=garagem,
            timestamp__date=data
        ).order_by('timestamp')

        resultado = []
        for acao in acoes:
            local_time = acao.timestamp.astimezone(FUSO_BRASIL)
            resultado.append({
                'acao': acao.action,
                'garagem': GARAGE_LABELS.get(acao.garage, acao.garage),  # Aqui troca pelo nome legível
                'horario': local_time.strftime('%H:%M:%S')
            })

        return JsonResponse({'historico': resultado})
    except Exception as e:
        return JsonResponse({'error': f'Erro ao processar a data: {str(e)}'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def ajustar_quantidade(request, garage):
    try:
        if garage not in GARAGENS_VALIDAS:
            return JsonResponse({'error': 'Garagem inválida.'}, status=400)

        data = json.loads(request.body)
        nova_quantidade = int(data.get('quantidade'))
        usuario = data.get('usuario')
        senha = data.get('senha')

        if usuario != 'ddd' or senha != 'ddd':
            return JsonResponse({'error': 'Usuário ou senha inválidos.'}, status=403)

        entradas = CarAction.objects.filter(action='entrada', garage=garage).count()
        saidas = CarAction.objects.filter(action='saida', garage=garage).count()
        saldo_atual = entradas - saidas
        diferenca = nova_quantidade - saldo_atual

        acao = 'entrada' if diferenca > 0 else 'saida'
        for _ in range(abs(diferenca)):
            CarAction.objects.create(action=acao, garage=garage)

        return JsonResponse({'message': f'Quantidade ajustada para {nova_quantidade} na garagem {garage}.'})
    except Exception as e:
        return JsonResponse({'error': f'Erro no ajuste de quantidade: {str(e)}'}, status=400)
