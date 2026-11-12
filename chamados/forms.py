from django import forms
from .models import Chamado, Equipamento, Local, TipoOcorrencia

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['titulo', 'descricao_problema', 'local', 'equipamento', 'tipo_ocorrencia']

class ResolverChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['descricao_solucao']
        labels = {
            'descricao_solucao': 'Descrição da Solução Aplicada'
        }
        widgets = {
            'descricao_solucao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva detalhadamente como o problema foi resolvido...'}),
        }

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['descricao']
        labels = {'descricao': 'Descrição do Equipamento'}
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md p-2 w-full focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Notebook Dell'
            }),
        }

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['descricao']
        labels = {'descricao': 'Local / Sala / Setor Físico'}
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md p-2 w-full focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Laboratório de Informática 01 ou Sala dos Professores'
            }),
        }

class TipoOcorrenciaForm(forms.ModelForm):
    class Meta:
        model = TipoOcorrencia
        fields = ['descricao']
        labels = {'descricao': 'Tipo de Ocorrência'}
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'border border-gray-300 rounded-md p-2 w-full focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Sem acesso à Internet ou Projetor queimado'
            }),
        }