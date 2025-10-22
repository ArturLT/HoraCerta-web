from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory 
from .forms import AluguelForm, ItemAlugadoFormSet
from .models import Aluguel, ItemAlugado 
from django.db import transaction
from django.http import JsonResponse

@login_required
def listar_alugueis(request):
    alugueis = Aluguel.objects.filter(usuario=request.user)
    return render(request, 'itemAlugados/listar_alugueis.html', {'alugueis': alugueis})

@login_required
def novo_aluguel(request):
    if request.method == 'POST':
        form = AluguelForm(request.POST, usuario=request.user)
        formset = ItemAlugadoFormSet(request.POST, usuario=request.user)

        if form.is_valid() and formset.is_valid():
            aluguel = form.save(commit=False)
            aluguel.usuario = request.user
            aluguel.save()

            itens = formset.save(commit=False)
            for item in itens:
                item.aluguel = aluguel
                item.valor_diaria = item.item.diaria
                item.save()

            
            aluguel.total = aluguel.calcular_total()
            aluguel.save(update_fields=['total'])

            return redirect('items_alugados:listar_alugueis')
    else:
        form = AluguelForm(usuario=request.user)
        formset = ItemAlugadoFormSet(usuario=request.user)

    return render(request, 'itemAlugados/novo_aluguel.html', {'form': form, 'formset': formset})

@login_required
def detalhe_aluguel(request, pk):
    """Visualiza os detalhes de um Aluguel específico (somente leitura)."""
    # Garante que o usuário só acesse seus próprios aluguéis
    aluguel = get_object_or_404(Aluguel, pk=pk, usuario=request.user)
    
    # Cria o formulário principal e o formset para exibição.
    # Usamos 'instance' para pré-preencher com os dados existentes.
    form = AluguelForm(instance=aluguel, usuario=request.user)
    
    # Cria uma classe base de formset ligada aos itens do aluguel
    # queryset: filtra os itens associados a este aluguel
    ItemAlugadoFormSetView = modelformset_factory(ItemAlugado, fields=('item', 'quantidade', 'valor_diaria'), extra=0)
    formset = ItemAlugadoFormSetView(queryset=ItemAlugado.objects.filter(aluguel=aluguel))
    
    return render(request, 'itemAlugados/detalhe_aluguel.html', {
        'aluguel': aluguel,
        'form': form,
        'formset': formset,
        'read_only': True # Passa uma flag para o template desabilitar inputs
    })


@login_required
def editar_aluguel(request, pk):
    """Edita um Aluguel e seus ItemAlugado associados."""
    aluguel = get_object_or_404(Aluguel, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        # Instancia os formulários com os dados POST e a instância existente
        form = AluguelForm(request.POST, instance=aluguel, usuario=request.user)
        # O formset precisa da instância do Aluguel para saber quais itens editar
        formset = ItemAlugadoFormSet(request.POST, instance=aluguel, usuario=request.user)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic(): # Garante que a operação seja atômica
                aluguel = form.save()
                
                # Salva os itens (cria novos, atualiza existentes, marca DELETE)
                itens = formset.save(commit=False)
                for item in itens:
                    item.aluguel = aluguel
                    # Recalcula a diária caso tenha sido alterado o item no select
                    item.valor_diaria = item.item.diaria 
                    item.save()
                
                # Para itens marcados para DELETAR
                formset.save_m2m() # Importante para relacionamentos ManyToMany (se houver, mas boa prática)
                
                # Recalcula e salva o total
                aluguel.total = aluguel.calcular_total()
                aluguel.save(update_fields=['total'])

            return redirect('items_alugados:listar_alugueis')
    else:
        # GET: Preenche os formulários com os dados atuais
        form = AluguelForm(instance=aluguel, usuario=request.user)
        formset = ItemAlugadoFormSet(instance=aluguel, usuario=request.user)

    return render(request, 'itemAlugados/editar_aluguel.html', {
        'form': form, 
        'formset': formset,
        'aluguel': aluguel
    })

@login_required
def excluir_aluguel(request, pk):
    aluguel = get_object_or_404(Aluguel, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        # Se você estiver usando AJAX, a resposta abaixo é apenas para fins de protocolo,
        # mas o AJAX espera um código de sucesso (200, 204). 
        try:
            with transaction.atomic():
                aluguel.delete()
                # Retorna uma resposta de sucesso para o AJAX
                return JsonResponse({'status': 'ok'}, status=200) 
        except Exception as e:
            # Retorna uma resposta de erro para o AJAX
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Se a requisição GET for enviada acidentalmente, apenas retorna a lista.
    return redirect('items_alugados:listar_alugueis')