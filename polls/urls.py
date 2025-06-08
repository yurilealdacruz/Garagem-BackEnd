from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entrada/<str:garage>/', views.entrada, name='entrada'),  # Ex: /entrada/A/ ou /entrada/B/
    path('saida/<str:garage>/', views.saida, name='saida'),        # Ex: /saida/A/ ou /saida/B/
    path('carros_na_garagem/<str:garage>/', views.carros_na_garagem, name='carros_na_garagem'),  # Ex: /carros_na_garagem/A/ ou /carros_na_garagem/B/
    path('limpar_dados/', views.limpar_dados, name='limpar_dados'),
    path('ajustar_quantidade/<str:garage>/', views.ajustar_quantidade, name='ajustar_quantidade'),
    path('api/historico/<str:garagem>/<str:data_str>/', views.historico_por_data),


]
