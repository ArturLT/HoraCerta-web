from django.shortcuts import render, redirect
# Importe a função login do Django e renomeie-a para evitar conflito
from django.contrib.auth import authenticate, login as django_login
from django.http.response import HttpResponse
from .models import User
from django.urls import reverse

def cadastro(request):
    if request.method == "GET":
        return render(request, 'accounts/cadastro.html')
    else:
        # Seu código de cadastro
        # ...
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        nome_empresa = request.POST.get('nome_empresa')

        usuario_existente = User.objects.filter(email=email).first()

        if usuario_existente:
            return HttpResponse("Email já existe")

        user = User.objects.create_user(nome=nome, email=email, senha=senha, nome_empresa=nome_empresa)
        
        return HttpResponse('Usuario cadastrado com sucesso')
    
def login(request):
    if request.method == "POST":
        identificador = request.POST.get('identificador')
        senha = request.POST.get('senha')

        usuario = authenticate(request, username=identificador, password=senha)
        
        if usuario is not None:
            django_login(request, usuario)
            # CORREÇÃO: Mude 'dashboard' para 'finance_list'
            return redirect(reverse('finance:finance_list'))
        else:
            return HttpResponse("Usuário ou senha inválidos.")
    else:
        return render(request, 'accounts/login.html')