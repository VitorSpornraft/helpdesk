from django import forms
from .models import Chamado

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