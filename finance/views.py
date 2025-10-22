from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import ItemForm
import calendar
from datetime import datetime
from django.db.models.functions import ExtractYear
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST


@login_required
def Dashboard(request):
    receitas_queryset = Item.objects.all().filter(tipo='receita')
    despesas_queryset = Item.objects.all().filter(tipo='despesa')

    total_receitas = receitas_queryset.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas_queryset.aggregate(Sum('valor'))['valor__sum'] or 0
    
    
    saldo = total_receitas - total_despesas

    context ={
        'receitas': total_receitas, 
        'despesas': total_despesas, 
        'saldo': saldo,
    }
    return render(request, 'finance/Dashboard.html', context)

@login_required
def total_despesas_receitas(request):
    total_receita = Item.objects.all().filter(tipo='receita')
    total_despesas = Item.objects.all().filter(tipo='despesa')

    soma_receita = total_receita.aggregate(Sum('total'))[total_receita]
    soma_despesas = total_despesas.aggregate(Sum('total'))[total_despesas]

    if request.method == "GET":
        return JsonResponse({'soma_receita': soma_receita, 'soma_despesas': soma_despesas})

@login_required
def Filtragem(request):
    usuario_logado = request.user
    base_queryset = Item.objects.filter(usuario=usuario_logado).order_by('data_transacao')
    base_queryset_ano = Item.objects.filter(usuario=request.user)

    anos_disponiveis = (
    base_queryset_ano
    .annotate(ano=ExtractYear('data_transacao'))  
    .values_list('ano', flat=True)                
    .distinct()                                   
    .order_by('-ano')                             
    )

    period_month = request.GET.get('filter_month')  
    period_year = request.GET.get('filter_year')    

    data_inicio = None
    data_fim = None

    if period_year:
        ano = int(period_year)

        if period_month:
            mes = int(period_month)
            data_inicio = datetime(ano, mes, 1)
            ultimo_dia = calendar.monthrange(ano, mes)[1]
            data_fim = datetime(ano, mes, ultimo_dia)
        else:
            data_inicio = datetime(ano, 1, 1)
            data_fim = datetime(ano, 12, 31)

    if data_inicio and data_fim:
        itens_filtrados = base_queryset.filter(
            data_transacao__gte=data_inicio,
            data_transacao__lte=data_fim
        )
    else:
        itens_filtrados = base_queryset

    context = {
    'itens': itens_filtrados,
    'current_month': period_month or "",
    'current_year': period_year or "",
    'anos_disponiveis': anos_disponiveis,
    }

    return render(request, 'finance/Receita_Despesas.html', context)


@login_required
def item_create(request):
    # (Permanece igual)
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

@login_required
def relario(request):
    usuario = request.user
    receitas = Item.objects.filter(tipo='receita', usuario=usuario)
    despesas = Item.objects.filter(tipo='despesa', usuario=usuario)

    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data1, data2, labels = [], [], []

    mes = datetime.now().month + 1
    ano = datetime.now().year

    for _ in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1

        r_total = receitas.filter(data_transacao__month=mes, data_transacao__year=ano).aggregate(Sum('valor'))['valor__sum'] or 0
        d_total = despesas.filter(data_transacao__month=mes, data_transacao__year=ano).aggregate(Sum('valor'))['valor__sum'] or 0

        labels.append(meses[mes - 1])
        data1.append(r_total)
        data2.append(d_total)

    return JsonResponse({
        'data1': data1[::-1],
        'data2': data2[::-1],
        'labels': labels[::-1]
    })

@login_required
@require_POST  # garante que só aceita POST
def item_delete(request, pk):
    # Pega o item ou retorna 404 se não existir ou não for do usuário
    item = get_object_or_404(Item, pk=pk, usuario=request.user)
    item.delete()
    messages.success(request, "Item deletado com sucesso!")
    return redirect('finance:finance_list')


@login_required
@require_POST
def item_delete_ajax(request, pk):
    item = get_object_or_404(Item, pk=pk, usuario=request.user)
    item.delete()
    return JsonResponse({'success': True, 'item_id': pk})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('finance:finance_list')
    else:
        form = ItemForm(instance=item)

    return render(request, 'finance/item_edit.html', {'form': form, 'item': item})
