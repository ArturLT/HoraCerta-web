from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
from .models import Cliente

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    return render(request, 'clients/listar_clientes.html', {'clientes': clientes})

@login_required
def criar_cliente(request):
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            novo_cliente = formulario.save(commit=False)
            novo_cliente.usuario = request.user
            novo_cliente.save()
            return redirect('clientes:cliente_list')
    else:
        formulario = ClienteForm()
    return render(request, 'clients/cliente_form.html', {'formulario': formulario})
