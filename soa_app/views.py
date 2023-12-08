from django import forms
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import DniInfo
import requests
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import openai
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed


class RucForm(forms.Form):
    ruc = forms.CharField(label='Número de RUC', max_length=11, required=True)
    razon_social = forms.CharField(label='Razón Social', max_length=255, required=False)
    estado = forms.CharField(label='Estado', max_length=50, required=False)
    condicion = forms.CharField(label='Condición', max_length=50, required=False)
    direccion = forms.CharField(label='Dirección', max_length=255, required=False)
    departamento = forms.CharField(label='Departamento', max_length=50, required=False)
    provincia = forms.CharField(label='Provincia', max_length=50, required=False)
    distrito = forms.CharField(label='Distrito', max_length=50, required=False)
    ubigeo = forms.CharField(label='Ubigeo', max_length=6, required=False)

def ruc_info(request):
    if request.method == 'POST':
        ruc = request.POST.get('ruc')
        url = f'https://dniruc.apisperu.com/api/v1/ruc/{ruc}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFsZXhhbmRlcnNrMjAxOUBnbWFpbC5jb20ifQ.qTHRcHFhIU0LuI06lYJWuARn3aozodTA7V5g2baKRIs'
        response = requests.get(url)
        data = response.json()

        form = RucForm(initial={
            'ruc': ruc,
            'razon_social': data['razonSocial'],
            'estado': data['estado'],
            'condicion': data['condicion'],
            'direccion': data['direccion'],
            'departamento': data['departamento'],
            'provincia': data['provincia'],
            'distrito': data['distrito'],
            'ubigeo': data['ubigeo'],
        })
    else:
        form = RucForm()

    return render(request, 'soa_app/ruc_info.html', {'form': form})

class DniForm(forms.Form):
    dni = forms.CharField(label='Número de DNI', max_length=8, required=True)
    nombres = forms.CharField(label='Nombres', max_length=255, required=False)
    apellido_paterno = forms.CharField(label='Apellido Paterno', max_length=255, required=False)
    apellido_materno = forms.CharField(label='Apellido Materno', max_length=255, required=False)
    cod_verifica = forms.IntegerField(label='Código de Verificación', required=False)
    correo = forms.EmailField(label='Correo', max_length=255, required=True)
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)

def dni_info(request):
    form = DniForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        dni = form.cleaned_data['dni']
        url = f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFsZXhhbmRlcnNrMjAxOUBnbWFpbC5jb20ifQ.qTHRcHFhIU0LuI06lYJWuARn3aozodTA7V5g2baKRIs'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            nombres = data.get('nombres', '')
            apellido_paterno = data.get('apellidoPaterno', '')
            apellido_materno = data.get('apellidoMaterno', '')
            cod_verifica = data.get('codVerifica', '')

            # Obtener datos del formulario
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

      

            # Crear o actualizar el objeto DniInfo
            obj, created = DniInfo.objects.update_or_create(
                dni=dni,
                defaults={
                    'nombres': nombres,
                    'apellido_paterno': apellido_paterno,
                    'apellido_materno': apellido_materno,
                    'cod_verifica': cod_verifica,
                    'correo': correo,
                    'contrasena': contrasena,
                }
            )

            return redirect('listar_dni_info')

    return render(request, 'soa_app/dni_info.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        try:
            dni_info = DniInfo.objects.get(correo=correo)
        except DniInfo.DoesNotExist:
            # El usuario no existe
            messages.error(request, 'Correo incorrecto.')
            return redirect('iniciar_sesion')

        # Verificar la contraseña
        if check_password(contrasena, dni_info.contrasena):
            
                messages.success(request, 'Correo correcto.')
                return redirect('inicio')
        else:
            # Contraseña incorrecta
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('iniciar_sesion')

    return render(request, 'soa_app/iniciar_sesion.html')

def listar_dni_info(request):
    dni_info_list = DniInfo.objects.all()
    return render(request, 'soa_app/listar_dni_info.html', {'dni_info_list': dni_info_list})

def inicio(request):
    return render(request, 'soa_app/inicio.html')

def vacuna_info(request):
    return render(request, 'soa_app/vacuna_info.html')

def info_covid_pais(request):
    return render(request, 'soa_app/info_covid_pais.html')

def grafico_covid(request):
    return render(request, 'soa_app/grafico_covid.html')

def noticias(request):
    return render(request, 'soa_app/noticias.html')

def logout_view(request):
    logout(request)
    # Redirige a la página que desees después de cerrar sesión
    return render(request, 'soa_app/iniciar_sesion.html')



key = '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'
openai.api_key = key
modelo = 'gpt-3.5-turbo'

def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            messages = [
                {'role': 'system', 'content': 'dame una respuesta de 3 lineas'},
                {'role': 'user', 'content': user_message}
            ]
            try:
                respuesta = openai.ChatCompletion.create(
                    model=modelo,
                    messages=messages,
                    temperature=0.8,
                    max_tokens=1000
                )
                bot_response = respuesta['choices'][0]['message']['content']
                return JsonResponse({'response': bot_response})
            except openai.error.OpenAIError as e:
                # Manejar errores de OpenAI, por ejemplo, imprimir el error
                print(f"Error de OpenAI: {str(e)}")
                return HttpResponseBadRequest("Error de OpenAI")
        else:
            return HttpResponseBadRequest("El mensaje del usuario no puede estar vacío.")
    return render(request, 'soa_app/chatbot.html')


def noticias(request):
    # Agrega tu clave de acceso aquí
    api_key = '595d3d7b462c6e05db2e2fd008278d76'
    url = f'http://api.mediastack.com/v1/news?access_key={api_key}&languages=es'
    

    response = requests.get(url)
    data = response.json()

    noticias = data.get('data', [])

    return render(request, 'soa_app/noticias.html', {'noticias': noticias})


def Rpta_OpenAI(request):

    key='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'
    if request.method== 'POST':
        consulta = request.POST.get("openai_consulta")
    else:
        consulta=''

    openai.api_key = key
    modelo = 'gpt-3.5-turbo'
    
    mensajes = [
        {'role':'system','content':'dame una respuesta de 3 lineas'},
        {'role':'user', 'content':consulta}
        ]
    respuesta = openai.ChatCompletion.create(
        model = modelo,
        messages = mensajes,
        temperature = 0.8,
        max_tokens = 1000
    )
    return render(request, 'soa_app/openai_consulta.html', {'respuesta': respuesta['choices'][0]['message']['content']})