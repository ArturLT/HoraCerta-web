from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        formulario = ClienteForm(request.POST, instance=cliente)
        if formulario.is_valid():
            formulario.save()
            return redirect('clientes:cliente_list')
    else:
        formulario = ClienteForm(instance=cliente)
    return render(request, 'clients/cliente_form.html', {'formulario': formulario})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    cliente.delete()
    return redirect('clientes:cliente_list')
