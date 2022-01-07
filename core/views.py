from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import Evento
from django.http.response import Http404, JsonResponse


# Create your views here.

def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return redirect('/')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = dict()
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')

        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.titulo = titulo
                evento.local = local
                evento.save()
            # forma sem validação de usuário
            # Evento.objects.filter(id=id_evento).update(
            #     titulo=titulo,
            #     data_evento=data_evento,
            #     descricao=descricao,
            #     local=local)
        else:
            Evento.objects.create(
                titulo=titulo,
                data_evento=data_evento,
                descricao=descricao,
                usuario=usuario,
                local=local)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


def json_lista_evento(request, id_usuario):
    try:
        return JsonResponse(
            list(Evento.objects.filter(usuario=User.objects.get(id=id_usuario)).values('id', 'titulo')),
            safe=False)
    except Exception:
        raise Http404()
