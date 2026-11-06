from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Chamado
from .forms import ChamadoForm

@login_required
def lista_chamados_solicitante(request):
    chamados = Chamado.objects.filter(solicitante=request.user).order_by('-data_abertura')
    return render(request, 'chamados/solicitante/lista.html', {'chamados': chamados})

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
    chamados = Chamado.objects.filter(
        Q(estado='ABERTO') | 
        Q(estado='EM_ANDAMENTO', responsavel=request.user)
    ).order_by('data_abertura')
    
    return render(request, 'chamados/tecnico/fila.html', {'chamados': chamados})

@login_required
def assumir_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    
    if chamado.estado == 'ABERTO':
        chamado.responsavel = request.user
        chamado.estado = 'EM_ANDAMENTO'
        chamado.inicio_atendimento = timezone.now()
        chamado.save()
        
    return redirect('fila_chamados_tecnico')