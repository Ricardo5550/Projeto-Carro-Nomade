from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.form_login, name='login'),

    path('list-rent/', views.list_rent, name='list-rent'),

    path('form-client/', views.form_client, name='client-create'),

    path('form-logout/', views.form_logout, name='logout'),

    path('form-verificacao/', views.form_verificacao, name='verificar-codigo'),

    path('form-recuperacao/', views.form_recuperacao, name='pedir-recuperacao'),

    path('form-verificar-recuperacao/', views.form_verificar_recuperacao, name='validar-codigo-recuperacao'),

    path('form-nova-senha/', views.form_nova_senha, name='definir-nova-senha'), 

    path('form-automovel/', views.form_automovel, name='automovel-create'),

    path('form-rent/<int:id>/', views.form_rent, name='rent-create'),

    path('reports/', views.reports, name='reports'),
]