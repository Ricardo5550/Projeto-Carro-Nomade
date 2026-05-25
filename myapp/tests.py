from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class CadastroUsuarioTest(TestCase):
    def test_registro_via_post(self):
        
        dados_formulario = {
            'username': 'clienteteste',
            'nome': 'Cliente Teste da Silva',
            'email': 'teste@carronomade.com',
            'telefone': '11999999999',
            'password1': 'SenhaSegura123!',  
            'password2': 'SenhaSegura123!',  
            'termos': 'on',                  
            'privacidade': 'on'              
        }

        url_cadastro = reverse('client-create')
        response = self.client.post(url_cadastro, dados_formulario)

        usuario_existe = User.objects.filter(username='clienteteste').exists()
        self.assertTrue(usuario_existe)
        
        print("\n[SUCESSO] Teste View (POST): O formulário do Carro Nômade foi preenchido, enviado e validado!")
