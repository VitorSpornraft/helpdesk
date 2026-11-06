from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Chamado
from .forms import ChamadoForm, ResolverChamadoForm

@login_required
def lista_chamados_solicitante(request):
    aba = request.GET.get('aba', 'abertos')
    
    if aba == 'andamento':
        chamados = Chamado.objects.filter(solicitante=request.user, estado='EM_ANDAMENTO').order_by('-data_abertura')
    elif aba == 'concluidos':
        chamados = Chamado.objects.filter(solicitante=request.user, estado='CONCLUIDO').order_by('-data_abertura')
    else:
        chamados = Chamado.objects.filter(solicitante=request.user, estado='ABERTO').order_by('-data_abertura')
        
    return render(request, 'chamados/solicitante/lista.html', {'chamados': chamados, 'aba': aba})

@login_required
def novo_chamado_solicitante(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.solicitante = request.user
            chamado.save()
            return redirect('lista_chamados_solicitante')
    else:
        form = ChamadoForm()
        
    return render(request, 'chamados/solicitante/novo.html', {'form': form})

@login_required
def fila_chamados_tecnico(request):
    aba = request.GET.get('aba', 'abertos')
    
    if aba == 'meus':
        chamados = Chamado.objects.filter(estado='EM_ANDAMENTO', responsavel=request.user).order_by('data_abertura')
    elif aba == 'concluidos':
        chamados = Chamado.objects.filter(estado='CONCLUIDO', responsavel=request.user).order_by('-fim_atendimento')
    else:
        chamados = Chamado.objects.filter(estado='ABERTO').order_by('data_abertura')
        
    return render(request, 'chamados/tecnico/fila.html', {'chamados': chamados, 'aba': aba})

@login_required
def assumir_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    
    if chamado.estado == 'ABERTO':
        chamado.responsavel = request.user
        chamado.estado = 'EM_ANDAMENTO'
        chamado.inicio_atendimento = timezone.now()
        chamado.save()
        
    return redirect('fila_chamados_tecnico')

@login_required
def resolver_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id, responsavel=request.user, estado='EM_ANDAMENTO')
    
    if request.method == 'POST':
        form = ResolverChamadoForm(request.POST, instance=chamado)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.estado = 'CONCLUIDO'
            chamado.fim_atendimento = timezone.now()
            chamado.save()
            return redirect('fila_chamados_tecnico')
    else:
        form = ResolverChamadoForm(instance=chamado)
        
    return render(request, 'chamados/tecnico/resolver.html', {'form': form, 'chamado': chamado})