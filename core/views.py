from django.shortcuts import render

# Create your views here.
from core.models import Evento


def lista_eventos(request):
    usuario = request.user
    #evento = Evento.objects.filter(usuario=usuario)
    evento = Evento.objects.all()
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)
