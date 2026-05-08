from django import forms
from .models import Client, Automovel, RegisterRent
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

## Cadastra Cliente.
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)

    def __init__(self, *args, **kwargs): ## Adiciona.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

## Cadastra um Automóvel.
class AutomovelForm(forms.ModelForm):
    automovel = forms.ImageField(label="Automóvel",widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Automovel
        fields = '__all__'
        exclude = ('is_rented',)

    def __init__(self, *args, **kwargs): ## Adiciona.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

## Registra Locação do Automóvel.
class RegisterRentForm(forms.ModelForm):
    dt_start = forms.DateTimeField(label='Início', widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date',}))
    dt_end = forms.DateTimeField(label='Fim', widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date',}))

    class Meta:
        model = RegisterRent
        fields = '__all__'
        exclude = ('automovel', 'create_at',)

    def __init__(self, *args, **kwargs): ## Adiciona.
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'