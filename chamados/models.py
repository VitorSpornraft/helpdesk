from django.db import models
from django.contrib.auth.models import User


class Departamento(models.Model):
  descricao = models.CharField(
      max_length=50, verbose_name='Nome do Departamento'
  )

  def __str__(self):
    return self.descricao


class Cargo(models.Model):
  descricao = models.CharField(max_length=50, verbose_name='Nome do Cargo')
  departamento = models.ForeignKey(
      Departamento,
      on_delete=models.CASCADE,
      verbose_name='Departamento Padrão',
  )

  def __str__(self):
    return self.descricao


class PerfilUsuario(models.Model):
  user = models.OneToOneField(
      User, on_delete=models.CASCADE, verbose_name='Usuário de Acesso'
  )
  telefone = models.CharField(max_length=20, blank=True, null=True)
  cargo = models.ForeignKey(
      Cargo, on_delete=models.SET_NULL, null=True, blank=True
  )
  departamento = models.ForeignKey(
      Departamento, on_delete=models.SET_NULL, null=True, blank=True
  )

  def __str__(self):
    return self.user.get_full_name() or self.user.username


class Local(models.Model):
  descricao = models.CharField(
      max_length=100, verbose_name='Local / Sala / Setor Físico'
  )

  def __str__(self):
    return self.descricao


class Equipamento(models.Model):
  descricao = models.CharField(
      max_length=100, verbose_name='Descrição do Equipamento/Ativo'
  )

  def __str__(self):
    return self.descricao


class TipoOcorrencia(models.Model):
  descricao = models.CharField(
      max_length=100, verbose_name='Tipo de Ocorrência'
  )

  def __str__(self):
    return self.descricao


class Chamado(models.Model):
  ESTADO_CHOICES = [
      ('ABERTO', 'Aberto'),
      ('EM_ANDAMENTO', 'Em Andamento'),
      ('CONCLUIDO', 'Concluído'),
      ('CANCELADO', 'Cancelado'),
  ]

  titulo = models.CharField(max_length=150, verbose_name='Título do Chamado')
  data_abertura = models.DateTimeField(
      auto_now_add=True, verbose_name='Data de Abertura'
  )
  descricao_problema = models.TextField(
      verbose_name='Descrição Detalhada do Problema'
  )

  solicitante = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='chamados_solicitados',
      verbose_name='Solicitante',
  )
  responsavel = models.ForeignKey(
      User,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='chamados_atendidos',
      verbose_name='Técnico Responsável',
  )

  local = models.ForeignKey(
      Local, on_delete=models.CASCADE, verbose_name='Local da Ocorrência'
  )
  equipamento = models.ForeignKey(
      Equipamento,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      verbose_name='Equipamento Envolvido',
  )
  tipo_ocorrencia = models.ForeignKey(
      TipoOcorrencia, on_delete=models.CASCADE, verbose_name='Tipo de Ocorrência'
  )

  inicio_atendimento = models.DateTimeField(
      null=True, blank=True, verbose_name='Início do Atendimento'
  )
  fim_atendimento = models.DateTimeField(
      null=True, blank=True, verbose_name='Fim do Atendimento'
  )
  descricao_solucao = models.TextField(
      null=True, blank=True, verbose_name='Descrição da Solução'
  )

  estado = models.CharField(
      max_length=20, choices=ESTADO_CHOICES, default='ABERTO', verbose_name='Status'
  )

  def __str__(self):
    return f'#{self.id} - {self.titulo} ({self.estado})'
