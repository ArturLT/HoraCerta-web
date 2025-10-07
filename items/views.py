from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import aluguelForm
from .models import Item_aluguel

@login_required
def aluguel_list(request):
    itens = Item_aluguel.objects.filter(usuario=request.user)
    return render(request, 'items/aluguel_list.html', {'itens': itens})

@login_required
def criar_item(request):
    if request.method == 'POST':
        formulario = aluguelForm(request.POST)
        if formulario.is_valid():
            novo_item = formulario.save(commit=False)
            novo_item.usuario = request.user
            novo_item.save()
            return redirect('items:aluguel_list')
    else:
        formulario = aluguelForm()
    return render(request, 'items/aluguel_forms.html', {'formulario': formulario})
