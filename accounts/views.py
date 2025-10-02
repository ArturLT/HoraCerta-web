from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.http.response import HttpResponse
from .models import User

from django.contrib.auth import authenticate, login as django_login
from django.http.response import HttpResponse
from django.contrib.auth import login as django_login
from accounts.backends import EmailOrNomeBackend
from .models import User
from .backends import EmailOrNomeBackend
from django.db.models import Q
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
        
        return render(request, 'accounts/login.html')
    

def login(request):
    if request.method == "POST":
        identificador = request.POST.get('identificador')
        senha = request.POST.get('senha')

        usuario = authenticate(request, username=identificador, password=senha)
        
        if usuario is not None:
            django_login(request, usuario)
            return redirect(reverse('finance:finance_list'))
        else:
            return HttpResponse("Usuário ou senha inválidos.")
    else:
        return render(request, 'accounts/login.html')
    
        try:
            user = User.objects.get(Q(nome=identificador) | Q(email=identificador))
        except User.DoesNotExist:
            return render(request, 'accounts/login.html', {'error': 'Nome ou e-mail inválido'})

        if user.check_password(senha):
            user.backend = 'accounts.backends.EmailOrNomeBackend' 
            django_login(request, user)
            return redirect(reverse('finance:finance_list'))
        else:
            return render(request, 'accounts/login.html', {'error': 'Senha incorreta'})

    return render(request, 'accounts/login.html')

