"""
URL configuration for soa_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from soa_app.views import dni_info, iniciar_sesion,  listar_dni_info, inicio, vacuna_info, info_covid_pais, grafico_covid, chatbot, logout_view, noticias, Rpta_OpenAI, ruc_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iniciar_sesion),
    path('dni_info/', dni_info, name='dni_info'),
    path('listar_dni_info/', listar_dni_info, name='listar_dni_info'),
    path('inicio/', inicio, name='inicio'),
    path('vacuna_info/', vacuna_info, name='vacuna_info'),
    path('info_covid_pais/', info_covid_pais, name='info_covid_pais'),
    path('grafico_covid/', grafico_covid, name='grafico_covid'),
    path('chatbot/', chatbot, name='chatbot'),
    path('', logout_view, name='logout'),
    path('noticias/', noticias, name='noticias'),
    path('openai_consulta/', Rpta_OpenAI, name='openai_consulta'),
    path('ruc_info/', ruc_info, name='ruc_info'),
]
