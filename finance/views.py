from django.shortcuts import render
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
from django.shortcuts import redirect

@login_required
def index(request):
    
    usuario_logado = request.user
    
    itens_do_usuario = Item.objects.filter(usuario=usuario_logado)
    
    context = {
        'itens': itens_do_usuario,
    }
    return render(request, 'finance/dashboard.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            novo_item = form.save(commit=False)
            novo_item.usuario = request.user
            novo_item.save()
            return redirect('finance:finance_list')
    else:
        form = ItemForm()
    
    return render(request, 'finance/item_create.html', {'form': form})