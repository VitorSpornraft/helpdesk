from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Count, Q   
from .models import Chamado, Equipamento, Local, TipoOcorrencia
from .forms import ChamadoForm, ResolverChamadoForm, EquipamentoForm, LocalForm, TipoOcorrenciaForm


# FUNÇÕES DE SEGURANÇA E CONTROLE DE ACESSO

def checa_se_tecnico_ou_noc(user):
    try:
        if not user.is_authenticated:
            return False
        perfil = user.perfilusuario
        return perfil.is_tecnico or perfil.is_noc
    except ObjectDoesNotExist:
        return False

def checa_se_noc(user):
    try:
        return user.is_authenticated and user.perfilusuario.is_noc
    except ObjectDoesNotExist:
        return False

# ÁREA DO SOLICITANTE

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

# ÁREA DO TÉCNICO E NOC

@login_required
@user_passes_test(checa_se_tecnico_ou_noc, login_url='lista_chamados_solicitante')
def fila_chamados_tecnico(request):
    aba = request.GET.get('aba', 'abertos')
    is_noc = request.user.perfilusuario.is_noc
    
    if aba == 'meus':
        if is_noc:
            chamados = Chamado.objects.filter(estado='EM_ANDAMENTO').order_by('data_abertura')
        else:
            chamados = Chamado.objects.filter(estado='EM_ANDAMENTO', responsavel=request.user).order_by('data_abertura')
            
    elif aba == 'concluidos':
        if is_noc:
            chamados = Chamado.objects.filter(estado='CONCLUIDO').order_by('-fim_atendimento')
        else:
            chamados = Chamado.objects.filter(estado='CONCLUIDO', responsavel=request.user).order_by('-fim_atendimento')
            
    else:
        chamados = Chamado.objects.filter(estado='ABERTO').order_by('data_abertura')
        
    return render(request, 'chamados/tecnico/fila.html', {'chamados': chamados, 'aba': aba, 'is_noc': is_noc})

@login_required
@user_passes_test(checa_se_tecnico_ou_noc, login_url='lista_chamados_solicitante')
def assumir_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    
    if chamado.estado == 'ABERTO':
        chamado.responsavel = request.user
        chamado.estado = 'EM_ANDAMENTO'
        chamado.inicio_atendimento = timezone.now()
        chamado.save()
        
    return redirect('fila_chamados_tecnico')

@login_required
@user_passes_test(checa_se_tecnico_ou_noc, login_url='lista_chamados_solicitante')
def resolver_chamado(request, chamado_id):
    is_noc = request.user.perfilusuario.is_noc
    
    if is_noc:
        chamado = get_object_or_404(Chamado, id=chamado_id, estado='EM_ANDAMENTO')
    else:
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

# CRUD DE EQUIPAMENTOS

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def lista_equipamentos(request):
    query = request.GET.get('q', '')
    if query:
        equipamentos = Equipamento.objects.filter(descricao__icontains=query)
    else:
        equipamentos = Equipamento.objects.all()
        
    return render(request, 'chamados/noc/lista_equipamentos.html', {'equipamentos': equipamentos, 'query': query})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def novo_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm()
    return render(request, 'chamados/noc/form_generico.html', {'form': form, 'titulo': 'Novo Equipamento', 'url_cancelar': 'lista_equipamentos'})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('lista_equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento)
    return render(request, 'chamados/noc/form_generico.html', {'form': form, 'titulo': 'Editar Equipamento', 'url_cancelar': 'lista_equipamentos'})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == 'POST':
        equipamento.delete()
        return redirect('lista_equipamentos')
    return render(request, 'chamados/noc/confirma_exclusao.html', {'item': equipamento.descricao, 'url_cancelar': 'lista_equipamentos'})

# CRUD DE LOCAIS

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def lista_locais(request):
    query = request.GET.get('q', '')
    if query:
        locais = Local.objects.filter(descricao__icontains=query)
    else:
        locais = Local.objects.all()
    return render(request, 'chamados/noc/lista_locais.html', {'locais': locais, 'query': query})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def novo_local(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_locais')
    else:
        form = LocalForm()
    return render(request, 'chamados/noc/form_generico.html', {'form': form, 'titulo': 'Novo Local', 'url_cancelar': 'lista_locais'})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def editar_local(request, id):
    local = get_object_or_404(Local, id=id)
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            return redirect('lista_locais')
    else:
        form = LocalForm(instance=local)
    return render(request, 'chamados/noc/form_generico.html', {'form': form, 'titulo': 'Editar Local', 'url_cancelar': 'lista_locais'})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def excluir_local(request, id):
    local = get_object_or_404(Local, id=id)
    if request.method == 'POST':
        local.delete()
        return redirect('lista_locais')
    return render(request, 'chamados/noc/confirma_exclusao.html', {'item': local.descricao, 'url_cancelar': 'lista_locais'})

# CRUD DE TIPOS DE OCORRÊNCIA

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def lista_tipos(request):
    query = request.GET.get('q', '')
    if query:
        tipos = TipoOcorrencia.objects.filter(descricao__icontains=query)
    else:
        tipos = TipoOcorrencia.objects.all()
    return render(request, 'chamados/noc/lista_tipos.html', {'tipos': tipos, 'query': query})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def novo_tipo(request):
    if request.method == 'POST':
        form = TipoOcorrenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipos')
    else:
        form = TipoOcorrenciaForm()
    return render(request, 'chamados/noc/form_generico.html', {'form': form, 'titulo': 'Novo Tipo de Ocorrência', 'url_cancelar': 'lista_tipos'})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def editar_tipo(request, id):
    tipo = get_object_or_404(TipoOcorrencia, id=id)
    if request.method == 'POST':
        form = TipoOcorrenciaForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('lista_tipos')
    else:
        form = TipoOcorrenciaForm(instance=tipo)
    return render(request, 'chamados/noc/form_generico.html', {'form': form, 'titulo': 'Editar Tipo de Ocorrência', 'url_cancelar': 'lista_tipos'})

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def excluir_tipo(request, id):
    tipo = get_object_or_404(TipoOcorrencia, id=id)
    if request.method == 'POST':
        tipo.delete()
        return redirect('lista_tipos')
    return render(request, 'chamados/noc/confirma_exclusao.html', {'item': tipo.descricao, 'url_cancelar': 'lista_tipos'})

# DASHBOARD DO NOC

@login_required
@user_passes_test(checa_se_noc, login_url='lista_chamados_solicitante')
def dashboard_noc(request):
    total_chamados = Chamado.objects.count()
    total_abertos = Chamado.objects.filter(estado='ABERTO').count()
    total_andamento = Chamado.objects.filter(estado='EM_ANDAMENTO').count()
    total_concluidos = Chamado.objects.filter(estado='CONCLUIDO').count()

    chamados_por_tipo = TipoOcorrencia.objects.annotate(
        total=Count('chamado')
    ).filter(total__gt=0).order_by('-total')

    pivot_locais = Local.objects.annotate(
        total_abertos=Count('chamado', filter=Q(chamado__estado='ABERTO')),
        total_andamento=Count('chamado', filter=Q(chamado__estado='EM_ANDAMENTO')),
        total_concluidos=Count('chamado', filter=Q(chamado__estado='CONCLUIDO')),
        total_geral=Count('chamado')
    ).filter(total_geral__gt=0).order_by('-total_geral')

    context = {
        'total_chamados': total_chamados,
        'total_abertos': total_abertos,
        'total_andamento': total_andamento,
        'total_concluidos': total_concluidos,
        'chamados_por_tipo': chamados_por_tipo,
        'pivot_locais': pivot_locais,
    }
    return render(request, 'chamados/noc/dashboard.html', context)