from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import ClientForm, AutomovelForm, RegisterRentForm, CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from .utils import send_code_email
from core.settings import EMAIL_HOST_USER
import secrets
import logging
logger = logging.getLogger('django_auditoria')
from datetime import timedelta
from django.utils import timezone
from .models import Automovel, AutomovelImage, CodigoVerificacao, ControleAcesso, CodigoRecuperacao, LogAuditoria

# Create your views here.
@login_required
def list_rent(request):
    automoveis = Automovel.objects.filter(is_rented=False)
    context = {'automoveis': automoveis}
    return render(request, 'list-rent.html', context)

def form_client(request):
    u_form = CustomUserCreationForm()
    c_form = ClientForm()
    if request.method == 'POST':
        u_form = CustomUserCreationForm(request.POST)
        c_form = ClientForm(request.POST)
        if u_form.is_valid() and c_form.is_valid():
            user = u_form.save()
            client = c_form.save(commit=False)
            client.user = user
            client.save()
            return redirect('login')
    return render(request, 'form-client.html', {'u_form': u_form, 'c_form': c_form})

def form_login(request):
    form = CustomLoginForm()

    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)

        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            controle_acesso, created = ControleAcesso.objects.get_or_create(user=user)
            if controle_acesso.bloqueado_ate:

                if timezone.now() < controle_acesso.bloqueado_ate:
                    return render(request, 'form-login.html', {'login_form': form, 'error': 'Acesso bloqueado. Tente novamente após 5 minutos.'})
            
                else:
                    controle_acesso.counter = 0
                    controle_acesso.bloqueado_ate = None
                    controle_acesso.save()
            
        if form.is_valid():
           # user = form.get_user()
            login(request, user)

            controle_acesso, created = ControleAcesso.objects.get_or_create(user=user)
            controle_acesso.counter = 0
            controle_acesso.bloqueado_ate = None
            controle_acesso.save()

            codigo_gerado = secrets.SystemRandom().randint(100000, 999999)

            send_code_email(
                user.username,
                codigo_gerado,
                EMAIL_HOST_USER,
                user.client.email
            )

            CodigoVerificacao.objects.create(
                codigo=codigo_gerado,
                user=user,
                expira_em=timezone.now() + timedelta(minutes=5)
            )

            return redirect('verificar-codigo')
        
        else:
            if user:
                controle_acesso, created = ControleAcesso.objects.get_or_create(user=user)
                controle_acesso.counter += 1

                if controle_acesso.counter >= 5:
                    controle_acesso.bloqueado_ate = timezone.now() + timedelta(minutes=5)
                
                controle_acesso.save()

    return render(request, 'form-login.html', {'login_form': form})

def form_verificacao(request):
    if request.method == 'POST':
        codigo_input = request.POST.get('codigo')
        user = request.user

        try:
            codigo_obj = CodigoVerificacao.objects.get(user=user, codigo=codigo_input)
            if codigo_obj.expira_em > timezone.now():
                login(request, codigo_obj.user)
                codigo_obj.delete()
                return redirect('list-rent')
            else:
                codigo_obj.delete()
                logout(request)
                return redirect('login')
        except CodigoVerificacao.DoesNotExist:
            return render(request, 'form-verificacao.html', {'error': 'Código inválido.'})

    return render(request, 'form-verificacao.html')

def form_recuperacao(request):
    if request.method == 'GET':
        return render(request, 'form-recuperacao.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            codigo_gerado = secrets.SystemRandom().randint(100000, 999999)

            send_code_email(
                user.username,
                codigo_gerado,
                EMAIL_HOST_USER,
                user.client.email
            )

            LogAuditoria.objects.create(
                usuario=user,
                acao="SOLICITAÇÃO",
                descricao="Solicitação de recuperação de senha iniciada. Código enviado por e-mail."
            )

            logger.info(f"Solicitação de recuperação de senha iniciada para o usuário: {user.username}")

            CodigoRecuperacao.objects.create(
                codigo=codigo_gerado,
                user=user,
                expira_em=timezone.now() + timedelta(minutes=5)
            )

            return redirect('validar-codigo-recuperacao')
        
        else:
            return render(request, 'form-recuperacao.html', {'error': 'Nome de Usuário não encontrado.'})

    return render(request, 'form-recuperacao.html')

def form_verificar_recuperacao(request):
    if request.method == 'GET':
        return render(request, 'verificar-recuperacao.html')
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        try:
            codigo_obj = CodigoRecuperacao.objects.get(codigo=codigo)
            if codigo_obj.expira_em > timezone.now():
                request.session['recuperacao_user_id'] = codigo_obj.user.id
                codigo_obj.delete()

                LogAuditoria.objects.create(
                    usuario=codigo_obj.user,
                    acao="VERIFICAÇÃO_SUCESSO",
                    descricao="Código de segurança inserido e validado com sucesso."
                )

                logger.info(f"Código de segurança validado com sucesso para o usuário: {codigo_obj.user.username}")

                return redirect('definir-nova-senha')
            else:
                codigo_obj.delete()

                LogAuditoria.objects.create(
                    usuario=codigo_obj.user,
                    acao="VERIFICAÇÃO_FALHA",
                    descricao="Tentativa de validação com código expirado."
                )

                logger.warning(f"Código de segurança expirado para o usuário: {codigo_obj.user.username}")
                
                return render(request, 'verificar-recuperacao.html', {'error': 'Código expirado.'})

        except CodigoRecuperacao.DoesNotExist:

            LogAuditoria.objects.create(
                usuario=None,
                acao="VERIFICAÇÃO_FALHA",
                descricao="Tentativa de validação com código inválido."
            )

            logger.warning(f"Tentativa de código de segurança inválido para o usuário: {codigo}")

            return render(request, 'verificar-recuperacao.html', {'error': 'Código inválido.'})

    return render(request, 'verificar-recuperacao.html')

def form_nova_senha(request):
    user_id = request.session.get('recuperacao_user_id')

    if not user_id:
        return redirect('login')

    if request.method == 'GET':
        return render(request, 'nova-senha.html')
    
    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        confirmacao_senha = request.POST.get('confirmar_senha')

        if nova_senha != confirmacao_senha:

            LogAuditoria.objects.create(
                usuario=User.objects.get(id=user_id),
                acao="REDEFINIÇÃO_FALHA",
                descricao="Tentativa de redefinição de senha com senhas não coincidentes."
            )

            logger.warning(f"Tentativa de redefinição de senha com senhas não coincidentes para o usuário: {user_id}")

            return render(request, 'nova-senha.html', {'error': 'As senhas não coincidem.'})

        try:
            user = User.objects.get(id=user_id)
            user.set_password(nova_senha)
            user.save()

            LogAuditoria.objects.create(
                usuario=user,
                acao="REDEFINIÇÃO_SUCESSO",
                descricao="Senha redefinida com sucesso no Banco de Dados com hash criptográfico."
            )

            logger.info(f"Senha redefinida com sucesso para o usuário: {user.username}")
            
            del request.session['recuperacao_user_id']
            return redirect('login')
        except User.DoesNotExist:
            return redirect('pedir-recuperacao')
        
def form_termos_uso(request):
    return render(request, 'termos-uso.html')

def form_politica_privacidade(request):
    return render(request, 'politica-privacidade.html')

@login_required
def form_perfil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = request.user

        user.username = username

        user.client.nome = nome_completo

        user.client.email = email

        if senha:
            user.set_password(senha)

            update_session_auth_hash(request, user)

        user.save()
        user.client.save()

        return redirect('perfil')

    return render(request, 'form-perfil.html')

@login_required
def form_excluir_conta(request):
    user = request.user
    user.delete()
    return redirect('login')

@login_required
def form_logout(request):
    logout(request)
    return redirect('login')

@login_required
def form_automovel(request):
    form = AutomovelForm()
    if request.method == 'POST':
        form = AutomovelForm(request.POST, request.FILES)
        if form.is_valid():
            automovel = form.save()
            files = request.FILES.getlist('automovel') ## Pega todas as imagens.
            if files:
                for f in files:
                    AutomovelImage.objects.create( ## Cria instância para imagens.
                        automovel=automovel,
                        image=f)
            return redirect('list-rent')
    return render(request, 'form-automovel.html', {'form': form})

@login_required
def form_rent(request, id):
    get_rented = Automovel.objects.get(id=id) ## Pega objeto.
    form = RegisterRentForm()
    if request.method == 'POST':
        form = RegisterRentForm(request.POST)
        if form.is_valid():
            rent_form = form.save(commit=False)
            rent_form.automovel = get_rented ## Salva id do automóvel.
            rent_form.save()

            ## Muda status do automóvel para "Alugado".
            automovel = Automovel.objects.get(id=id)
            automovel.is_rented = True ## Passa a ser True.
            automovel.save()
            return redirect('list-rent') ## Retorna para a Lista.
        
    context = {'form': form, 'rent': get_rented}
    return render(request, 'form-rent.html', context)

## Relatório.
@login_required
def reports(request): ## Relatórios.
    automovel = Automovel.objects.all()

    get_client = request.GET.get('client')
    get_rented = request.GET.get('is_rented')
    get_category = request.GET.get('category')
    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')
    print(get_dt_end, get_dt_start)

    if get_client: ## Filtra por nome e e-mail do cliente.
        automovel = Automovel.objects.filter(
            Q(reg_rent__client__nome__icontains=get_client) | 
            Q(reg_rent__client__email__icontains=get_client))
        
    if get_dt_start and get_dt_end: ## Por data.
        automovel = Automovel.objects.filter(
            reg_rent__create_at__range=[get_dt_start, get_dt_end])

    if get_rented:
        automovel = Automovel.objects.filter(is_rented=get_rented)

    if get_category:
        automovel = Automovel.objects.filter(category=get_category)

    return render(request, 'reports.html', {'automoveis': automovel})