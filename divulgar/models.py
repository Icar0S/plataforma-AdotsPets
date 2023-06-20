from django.db import models
from django.contrib.auth.models import User

class Raca(models.Model):
  raca = models.CharField(max_length=50)

  def __str__(self):
    return self.raca


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class Pet(models.Model):
    choices_status = (('P', 'Para adoção'),
                      ('A', 'Adotado'))
    
    choices_sexo = (('C', 'Castrado'),
                    ('M', 'Masculino'),
                    ('F', 'Feminino'))
    
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    foto = models.ImageField(upload_to="fotos_pets")
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=choices_sexo, default='C')
    
    #criando relacoes:
    # 1 pet tem varias tags, muitos para muitos.
    tags = models.ManyToManyField(Tag)
    # 1 pet tem 1 raça: um para um.
    raca = models.ForeignKey(Raca, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=choices_status, default='P')
    
    
    def __str__(self):
        return self.nome