from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.form_login, name='login'),

    path('list-rent/', views.list_rent, name='list-rent'),

    path('form-client/', views.form_client, name='client-create'),

    path('form-logout/', views.form_logout, name='logout'), 

    path('form-automovel/', views.form_automovel, name='automovel-create'),

    path('form-rent/<int:id>/', views.form_rent, name='rent-create'),

    path('reports/', views.reports, name='reports'),
]