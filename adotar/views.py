from django.shortcuts import render
from divulgar.models import Pet, Raca
from django.contrib.messages import constants
from django.contrib import messages
from .models import PedidoAdocao
from django.shortcuts import redirect
from datetime import datetime
from django.core.mail import send_mail

def listar_pets(request):
    if request.method == "GET":
      pets = Pet.objects.filter(status="P")
      racas = Raca.objects.all()
      
      sexo = request.GET.get('sexo')
      cidade = request.GET.get('cidade')
      raca_filter = request.GET.get('raca', None)
      
      if sexo:
          pets = pets.filter(sexo__icontains=sexo)
          raca_filter = None

      if cidade:
          pets = pets.filter(cidade__icontains=cidade)
          raca_filter = None
    
      if raca_filter is not None:
            if raca_filter == '14':
                pets = Pet.objects.filter()
                raca_filter = Raca.objects.all()
            else:
                pets = pets.filter(raca__id=raca_filter)
                raca_filter = Raca.objects.get(id=raca_filter)
      else:
        raca_filter = None

      return render(request, 'listar_pets.html', {'pets': pets, 'racas': racas, 'sexo':sexo, 'cidade': cidade, 'raca_filter': raca_filter})
    
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.ERROR, 'Esse pet já foi adotado :)')
        return redirect('/adotar')

    pedido = PedidoAdocao(pet=pet.first(),
            usuario=request.user,
            data=datetime.now())

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar')



def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    if status == "A":
        pedido.status = 'AP'
        string = '''Olá, sua adoção foi aprovada. ...'''
    elif status == "R":
        string = '''Olá, sua adoção foi recusada. ...'''
        pedido.status = 'R'

    pedido.save()

    #TODO alterar status do pet
    print(pedido.usuario.email)
    email = send_mail(
        'Sua adoção foi processada',
        string,
        'ongidopt@gmail.com.br',
        [pedido.usuario.email,],
    )
    
    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado com sucesso')
    return redirect('/divulgar/ver_pedido_adocao')