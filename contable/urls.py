from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'registro/', registro),
    url(r'login/', auth_views.login, {'template_name': 'contable/login.html'}),
    url(r'logout/', auth_views.logout),
    url(r'contable/', dashboard),
    url(r'perfil/', perfil),
    url(r'cuenta/', cuenta),
    url(r'editar_perfil/', perfil),
    url(r'editar_empresa/', editar_empresa),
    url(r'completar_empresa/', completar_empresa),
    url(r'comprobantes/', comprobantes),
    url(r'reporte/', reporte),
]
