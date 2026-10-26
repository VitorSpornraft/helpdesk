from django.contrib import admin
from .models import Departamento, Cargo, PerfilUsuario, Local, Equipamento, TipoOcorrencia, Chamado

admin.site.register(Departamento)
admin.site.register(Cargo)
admin.site.register(PerfilUsuario)
admin.site.register(Local)
admin.site.register(Equipamento)
admin.site.register(TipoOcorrencia)

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'solicitante', 'responsavel', 'estado', 'data_abertura')
    list_filter = ('estado', 'local', 'tipo_ocorrencia')
    search_fields = ('titulo', 'descricao_problema')
