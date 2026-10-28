from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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