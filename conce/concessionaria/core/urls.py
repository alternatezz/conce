from django.urls import path
from . import views

urlpatterns = [
    path('carros/', views.listar_carros, name='listar_carros'),
    path('registrar_venda/', views.registrar_venda, name='registrar_venda'),
    path('cadastrar_carro/', views.cadastrar_carro, name='cadastrar_carro'),
]
