from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import ClientForm, AutomovelForm, RegisterRentForm, CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Automovel, AutomovelImage

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
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list-rent')
    return render(request, 'form-login.html', {'login_form': form})

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