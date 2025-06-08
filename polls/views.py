from django.shortcuts import render
from django.http import JsonResponse
from .models import CarAction
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from datetime import datetime

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def entrada(request, garage):
    if request.method == 'POST':
        if garage in ['A', 'B']:  # Validação de garagem
            CarAction.objects.create(action='entrada', garage=garage)
            return JsonResponse({'message': f'Entrada registrada na Garagem {garage} com sucesso!'})
        return JsonResponse({'error': 'Garagem inválida.'}, status=400)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_exempt
def saida(request, garage):
    if request.method == 'POST':
        if garage in ['A', 'B']:  # Validação de garagem
            entradas = CarAction.objects.filter(action='entrada', garage=garage).count()
            saidas = CarAction.objects.filter(action='saida', garage=garage).count()
            carros_na_garagem = entradas - saidas

            if carros_na_garagem > 0:
                CarAction.objects.create(action='saida', garage=garage)
                return JsonResponse({'message': f'Saída registrada na Garagem {garage} com sucesso!'})
            else:
                return JsonResponse({'error': f'Não há carros suficientes na Garagem {garage} para saída.'}, status=400)
        return JsonResponse({'error': 'Garagem inválida.'}, status=400)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)

def carros_na_garagem(request, garage):
    if garage in ['A', 'B']:  # Validação de garagem
        entradas = CarAction.objects.filter(action='entrada', garage=garage).count()
        saidas = CarAction.objects.filter(action='saida', garage=garage).count()
        carros_na_garagem = entradas - saidas
        return JsonResponse({'carros_na_garagem': carros_na_garagem})
    return JsonResponse({'error': 'Garagem inválida.'}, status=400)

@csrf_exempt
def limpar_dados(request):
    if request.method == 'POST':
        CarAction.objects.all().delete()
        return JsonResponse({'message': 'Todos os registros foram apagados com sucesso!'})
    return JsonResponse({'error': 'Método não permitido.'}, status=405)


@csrf_exempt
@require_http_methods(["POST"])
def ajustar_quantidade(request, garage):
    try:
        data = json.loads(request.body)
        nova_quantidade = int(data.get('quantidade'))

        if garage not in ['A', 'B']:
            return JsonResponse({'error': 'Garagem inválida.'}, status=400)

        entradas = CarAction.objects.filter(action='entrada', garage=garage).count()
        saidas = CarAction.objects.filter(action='saida', garage=garage).count()
        saldo_atual = entradas - saidas

        diferenca = nova_quantidade - saldo_atual

        if diferenca > 0:
            # adicionar entradas
            for _ in range(diferenca):
                CarAction.objects.create(action='entrada', garage=garage)
        elif diferenca < 0:
            # adicionar saidas
            for _ in range(-diferenca):
                CarAction.objects.create(action='saida', garage=garage)

        return JsonResponse({'message': f'Quantidade ajustada para {nova_quantidade} na garagem {garage}.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@csrf_exempt
def historico_por_data(request, garagem, data_str):
    try:
        # Transforma '2024-06-08' em objeto datetime
        data = datetime.strptime(data_str, '%Y-%m-%d').date()

        # Filtra ações no mesmo dia e garagem
        acoes = CarAction.objects.filter(
            garage=garagem,
            timestamp__date=data
        ).order_by('timestamp')

        resultado = [
            {
                'acao': acao.action,
                'garagem': acao.get_garage_display(),
                'horario': acao.timestamp.strftime('%H:%M:%S')
            }
            for acao in acoes
        ]
        return JsonResponse({'historico': resultado})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)