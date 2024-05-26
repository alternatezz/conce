from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Carro, Venda

# Função para listar carros
def listar_carros(request):
    carros = Carro.objects.all()
    carros_list = [{'id': carro.id, 'marca': carro.marca, 'modelo': carro.modelo, 'ano': carro.ano, 'preco': carro.preco, 'cor': carro.cor} for carro in carros]
    return JsonResponse(carros_list, safe=False)

# Função para registrar uma venda
@csrf_exempt
def registrar_venda(request):
    if request.method == 'POST':
        carro_id = request.POST.get('carro_id')
        cliente_nome = request.POST.get('cliente_nome')
        carro = Carro.objects.get(pk=carro_id)
        valor_venda = carro.preco * 1.1
        Venda.objects.create(carro=carro, cliente_nome=cliente_nome, valor_venda=valor_venda)
        return JsonResponse({'message': 'Venda registrada com sucesso'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Função para cadastrar um carro
@csrf_exempt
def cadastrar_carro(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        ano = request.POST.get('ano')
        preco = request.POST.get('preco')
        cor = request.POST.get('cor')
        Carro.objects.create(marca=marca, modelo=modelo, ano=ano, preco=preco, cor=cor)
        return JsonResponse({'message': 'Carro cadastrado com sucesso'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)
