from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import aluguelForm
from .models import Item_aluguel
from django.shortcuts import get_object_or_404, redirect
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

# --- Editar item ---
@login_required
def editar_item(request, pk):
    item = get_object_or_404(Item_aluguel, pk=pk, usuario=request.user)
    if request.method == 'POST':
        formulario = aluguelForm(request.POST, instance=item)
        if formulario.is_valid():
            formulario.save()
            return redirect('items:aluguel_list')
    else:
        formulario = aluguelForm(instance=item)
    return render(request, 'items/aluguel_forms.html', {'formulario': formulario, 'editar': True})





@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item_aluguel, pk=pk, usuario=request.user)
    item.delete()
    return redirect('items:aluguel_list')


