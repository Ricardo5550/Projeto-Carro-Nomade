from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
## Cadastro de Clientes.
class Client(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', max_length=200)
    telefone = models.CharField('Telefone', max_length=15)

    def __str__(self):
        return "{} - {}".format(self.nome, self.email)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']

## Opções de Automóveis.
class TypeAutomovel(models.TextChoices):
    HATCH = 'HATCH', 'Hatch'
    SEDAN = 'SEDAN', 'Sedan'
    SUV = 'SUV', 'SUV'

## Cadastro de Automóveis.
class Automovel(models.Model):
    code = models.CharField('Código',max_length=100)
    category = models.CharField('Categoria do Automóvel', max_length=100, choices=TypeAutomovel.choices)
    model = models.CharField('Modelo', max_length=200)
    model_year = models.IntegerField('Ano do Modelo', blank=True, null=True)
    plate = models.CharField('Placa', max_length=10, blank=True, null=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    is_rented = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.code, self.category)
    
    class Meta:
        verbose_name = 'Automóvel'
        verbose_name_plural = 'Automóveis'
        ordering = ['-id']

## Cadastrar as Imagens do Automóvel.
class AutomovelImage(models.Model):
    image = models.ImageField('Images', upload_to='images')
    automovel = models.ForeignKey(Automovel, related_name='automovel_images', on_delete=models.CASCADE)

    def __str__(self):
        return self.automovel.code
    
## Registrar Aluguel.
class RegisterRent(models.Model):
    automovel = models.ForeignKey(Automovel, on_delete=models.CASCADE, related_name='reg_rent')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    dt_start = models.DateTimeField('Início')
    dt_end = models.DateTimeField('Fim')
    create_at = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return "{} - {}".format(self.client, self.automovel)
    
    class Meta:
        verbose_name = 'Registrar Aluguel'
        verbose_name_plural = 'Registrar Aluguéis'
        ordering = ['-id']