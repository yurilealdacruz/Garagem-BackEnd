from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Entradas e saídas
    path('entrada/<str:garage>/', views.entrada, name='entrada'),
    path('saida/<str:garage>/', views.saida, name='saida'),

    # Consulta de saldo atual
    path('carros_na_garagem/<str:garage>/', views.carros_na_garagem, name='carros_na_garagem'),

    # Histórico por data
    path('historico/<str:garagem>/<str:data_str>/', views.historico_por_data, name='historico'),

    # Limpeza e ajuste manual
    path('limpar_dados/', views.limpar_dados, name='limpar_dados'),
    path('ajustar_quantidade/<str:garage>/', views.ajustar_quantidade, name='ajustar_quantidade'),
]
