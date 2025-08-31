from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
import io
import base64
import numpy as np
import calendar

from .models import Categoria, Conta, Transacao
from .forms import CategoriaForm, ContaForm, TransacaoForm, RegistroForm

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('controle:dashboard')
    else:
        form = RegistroForm()
    return render(request, 'controle/registro.html', {'form': form})

@login_required
def dashboard(request):
    contas = Conta.objects.filter(usuario=request.user)
    saldo_total = contas.aggregate(total=Sum('saldo'))['total'] or 0
    
    # Transações recentes
    transacoes_recentes = Transacao.objects.filter(usuario=request.user).order_by('-data')[:5]
    
    # Resumo mensal
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    ultimo_dia_mes = (primeiro_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    receitas_mes = Transacao.objects.filter(
        usuario=request.user,
        categoria__tipo='R',
        data__range=[primeiro_dia_mes, ultimo_dia_mes]
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    despesas_mes = Transacao.objects.filter(
        usuario=request.user,
        categoria__tipo='D',
        data__range=[primeiro_dia_mes, ultimo_dia_mes]
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    # Dados para gráfico de despesas por categoria
    categorias_despesa = Categoria.objects.filter(usuario=request.user, tipo='D')
    dados_grafico = []
    labels = []
    cores = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#8AC249', '#EA526F', '#49ADF5', '#C8B0F5'
    ]
    
    for categoria in categorias_despesa:
        total = Transacao.objects.filter(
            usuario=request.user,
            categoria=categoria,
            data__range=[primeiro_dia_mes, ultimo_dia_mes]
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        if total > 0:
            dados_grafico.append(float(total))
            labels.append(categoria.nome)
    
    # Preparar dados para Chart.js
    dados_categorias = {
        'labels': labels,
        'datasets': [{
            'data': dados_grafico,
            'backgroundColor': cores[:len(dados_grafico)],
            'borderWidth': 1
        }]
    }
    
    context = {
        'contas': contas,
        'saldo_total': saldo_total,
        'transacoes_recentes': transacoes_recentes,
        'receitas_mes': receitas_mes,
        'despesas_mes': despesas_mes,
        'dados_categorias': dados_categorias,
    }
    
    return render(request, 'controle/dashboard.html', context)

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'controle/lista_categorias.html', {'categorias': categorias})

@login_required
def nova_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('controle:lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'controle/form_categoria.html', {'form': form})

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('controle:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'controle/form_categoria.html', {'form': form})

@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('controle:lista_categorias')
    return render(request, 'controle/confirmar_exclusao.html', {'objeto': categoria})

@login_required
def lista_contas(request):
    contas = Conta.objects.filter(usuario=request.user)
    return render(request, 'controle/lista_contas.html', {'contas': contas})

@login_required
def nova_conta(request):
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('controle:lista_contas')
    else:
        form = ContaForm()
    return render(request, 'controle/form_conta.html', {'form': form})

@login_required
def editar_conta(request, pk):
    conta = get_object_or_404(Conta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ContaForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta atualizada com sucesso!')
            return redirect('controle:lista_contas')
    else:
        form = ContaForm(instance=conta)
    return render(request, 'controle/form_conta.html', {'form': form})

@login_required
def excluir_conta(request, pk):
    conta = get_object_or_404(Conta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        conta.delete()
        messages.success(request, 'Conta excluída com sucesso!')
        return redirect('controle:lista_contas')
    return render(request, 'controle/confirmar_exclusao.html', {'objeto': conta})

@login_required
def lista_transacoes(request):
    transacoes = Transacao.objects.filter(usuario=request.user)
    return render(request, 'controle/lista_transacoes.html', {'transacoes': transacoes})

@login_required
def nova_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            messages.success(request, 'Transação registrada com sucesso!')
            return redirect('controle:lista_transacoes')
    else:
        form = TransacaoForm()
        # Filtrar categorias e contas do usuário
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=request.user)
        form.fields['conta'].queryset = Conta.objects.filter(usuario=request.user)
    return render(request, 'controle/form_transacao.html', {'form': form})

@login_required
def editar_transacao(request, pk):
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transação atualizada com sucesso!')
            return redirect('controle:lista_transacoes')
    else:
        form = TransacaoForm(instance=transacao)
        # Filtrar categorias e contas do usuário
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=request.user)
        form.fields['conta'].queryset = Conta.objects.filter(usuario=request.user)
    return render(request, 'controle/form_transacao.html', {'form': form})

@login_required
def excluir_transacao(request, pk):
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        transacao.delete()
        messages.success(request, 'Transação excluída com sucesso!')
        return redirect('controle:lista_transacoes')
    return render(request, 'controle/confirmar_exclusao.html', {'objeto': transacao})

@login_required
def relatorio_mensal(request):
    hoje = timezone.now().date()
    mes = request.GET.get('mes', hoje.month)
    ano = request.GET.get('ano', hoje.year)
    
    try:
        mes = int(mes)
        ano = int(ano)
        data_inicio = datetime(ano, mes, 1).date()
        if mes == 12:
            data_fim = datetime(ano + 1, 1, 1).date() - timedelta(days=1)
        else:
            data_fim = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
    except (ValueError, TypeError):
        mes = hoje.month
        ano = hoje.year
        data_inicio = datetime(ano, mes, 1).date()
        if mes == 12:
            data_fim = datetime(ano + 1, 1, 1).date() - timedelta(days=1)
        else:
            data_fim = datetime(ano, mes + 1, 1).date() - timedelta(days=1)
    
    receitas = Transacao.objects.filter(
        usuario=request.user,
        categoria__tipo='R',
        data__range=[data_inicio, data_fim]
    )
    
    despesas = Transacao.objects.filter(
        usuario=request.user,
        categoria__tipo='D',
        data__range=[data_inicio, data_fim]
    )
    
    total_receitas = receitas.aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or 0
    saldo_mensal = total_receitas - total_despesas
    
    # 1. Ajuste para o gráfico de evolução diária
    # Pega o saldo total da conta do usuário no dia anterior ao início do mês
    data_dia_anterior = data_inicio - timedelta(days=1)
    
    # Agrega receitas e despesas até o dia anterior para um cálculo mais eficiente
    saldo_inicial_mes = Transacao.objects.filter(
        usuario=request.user,
        data__lte=data_dia_anterior,
    ).aggregate(
        total_receitas=Sum('valor', filter=Q(categoria__tipo='R')),
        total_despesas=Sum('valor', filter=Q(categoria__tipo='D'))
    )

    # 2. Inicia o saldo acumulado com o valor do mês anterior
    saldo_acumulado = (saldo_inicial_mes['total_receitas'] or 0) - (saldo_inicial_mes['total_despesas'] or 0)
        
    # Pega todas as transações do mês e ordena por data para o cálculo diário
    transacoes_mes = Transacao.objects.filter(
        usuario=request.user,
        data__range=[data_inicio, data_fim]
    ).order_by('data')

    saldos_diarios = []
    labels_datas = []

    # 3. Itera sobre os dias do mês
    current_data = data_inicio
    while current_data <= data_fim:
        # Pega as transações do dia
        receita_dia = transacoes_mes.filter(
            categoria__tipo='R',
            data=current_data
        ).aggregate(total=Sum('valor'))['total'] or 0

        despesa_dia = transacoes_mes.filter(
            categoria__tipo='D',
            data=current_data
        ).aggregate(total=Sum('valor'))['total'] or 0

        # Atualiza o saldo acumulado
        saldo_acumulado += receita_dia - despesa_dia
        saldos_diarios.append(float(saldo_acumulado))
        labels_datas.append(current_data.strftime('%d/%m'))

        current_data += timedelta(days=1)

    # Preparar dados para Chart.js
    dados_evolucao = {
        'labels': labels_datas,
        'datasets': [{
            'label': 'Saldo Acumulado',
            'data': saldos_diarios,
            'borderColor': '#4BC0C0',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderWidth': 2,
            'fill': True,
            'tension': 0.4,
            'pointRadius': 4,
            'pointBackgroundColor': '#4BC0C0',
            'pointHoverRadius': 6,
            'pointHoverBackgroundColor': '#36A2EB',
            'pointHoverBorderColor': '#fff',
            'pointHoverBorderWidth': 2
        }]
    }
    
    # Calcular despesas por categoria para o mês
    categorias_despesa = Categoria.objects.filter(usuario=request.user, tipo='D')
    despesas_por_categoria = []
    
    for categoria in categorias_despesa:
        total = Transacao.objects.filter(
            usuario=request.user,
            categoria=categoria,
            data__range=[data_inicio, data_fim]
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        # Incluir todas as categorias, mesmo com valor zero
        despesas_por_categoria.append({
            'categoria': categoria.nome,
            'valor': float(total),
            'valor_formatado': f"{float(total):,.2f}".replace(',', '.').replace('.', ','),
            'percentual': 0  # Será calculado abaixo
        })

    despesas_por_categoria= sorted(despesas_por_categoria, key= lambda x: x['valor'], reverse=True)
    
    # Calcular percentuais
    total_despesas_valor = sum(item['valor'] for item in despesas_por_categoria)
    if total_despesas_valor > 0:
        for item in despesas_por_categoria:
            item['percentual'] = (item['valor'] / total_despesas_valor) * 100
    
    context = {
        'mes': mes,
        'ano': ano,
        'receitas': receitas,
        'despesas': despesas,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo_mensal': saldo_mensal,
        'dados_evolucao': dados_evolucao,
        'despesas_por_categoria': despesas_por_categoria,
    }
    
    return render(request, 'controle/relatorio_mensal.html', context)

@login_required
def ajax_criar_categoria(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            nome = request.POST.get('nome')
            tipo = request.POST.get('tipo')
            
            # Validar dados
            if not nome or not tipo:
                return JsonResponse({'success': False, 'error': 'Nome e tipo são obrigatórios'})
            
            if tipo not in ['D', 'R']:
                return JsonResponse({'success': False, 'error': 'Tipo inválido'})
            
            # Criar categoria
            categoria = Categoria.objects.create(
                nome=nome,
                tipo=tipo,
                usuario=request.user
            )
            
            return JsonResponse({
                'success': True,
                'categoria_id': categoria.id,
                'categoria_nome': categoria.nome
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


@login_required
def ajax_criar_conta(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            nome = request.POST.get('nome')
            saldo_inicial = request.POST.get('saldo_inicial', 0)
            
            # Validar dados
            if not nome:
                return JsonResponse({'success': False, 'error': 'Nome é obrigatório'})
            
            try:
                saldo_inicial = float(saldo_inicial)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Saldo inicial inválido'})
            
            # Criar conta
            conta = Conta.objects.create(
                nome=nome,
                saldo_inicial=saldo_inicial,
                usuario=request.user
            )
            
            return JsonResponse({
                'success': True,
                'conta_id': conta.id,
                'conta_nome': conta.nome
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
