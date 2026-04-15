from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from JB_Chopeiras.models import Servico
from JB_Chopeiras.serializer import ServicoSerializer
from JB_Chopeiras.formulario import ServicoFormulario

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser


class ServicoViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer


def servicosPage(request):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    servicos = Servico.objects.all()
    return render(request, 'servicosPage.html', {'servicos': servicos})


def criar_servico(request):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = ServicoFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicosPage')
    else:
        form = ServicoFormulario()

    return render(request, 'servico_formulario.html', {
        'form': form,
        'titulo': 'Criar Serviço'
    })


def editar_servico(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    servico = get_object_or_404(Servico, id=id)

    if request.method == 'POST':
        form = ServicoFormulario(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('servicosPage')
    else:
        form = ServicoFormulario(instance=servico)

    return render(request, 'servico_formulario.html', {
        'form': form,
        'titulo': 'Editar Serviço'
    })


def excluir_servico(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    servico = get_object_or_404(Servico, id=id)

    if request.method == 'POST':
        servico.delete()
        return redirect('servicosPage')

    return render(request, 'servico_confirmar_exclusao.html', {'servico': servico})


def home(request):
    return render(request, 'home.html')


def sair(request):
    logout(request)
    return redirect('home')


def tela_entrada(request):
    mensagem = None

    if request.method == 'POST':
        tipo_form = request.POST.get('tipo_form')

        if tipo_form == 'login':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('senha', '').strip()

            if not email or not senha:
                mensagem = 'Preencha email e senha.'
            else:
                try:
                    usuario_obj = User.objects.get(email=email)
                    usuario = authenticate(request, username=usuario_obj.username, password=senha)
                except User.DoesNotExist:
                    usuario = None

                if usuario is not None:
                    login(request, usuario)

                    if usuario.is_staff:
                        return redirect('servicosPage')
                    else:
                        return redirect('home')
                else:
                    mensagem = 'Usuário ou senha inválidos.'

        elif tipo_form == 'registro':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('senha', '').strip()
            confirmar_senha = request.POST.get('confirmar_senha', '').strip()

            if not email or not senha or not confirmar_senha:
                mensagem = 'Preencha todos os campos obrigatórios.'
            elif senha != confirmar_senha:
                mensagem = 'As senhas não coincidem.'
            elif User.objects.filter(username=email).exists():
                mensagem = 'Já existe um usuário com esse email.'
            else:
                usuario = User.objects.create_user(
                    username=email,
                    email=email,
                    password=senha
                )
                login(request, usuario)
                return redirect('home')

    return render(request, 'login.html', {'mensagem': mensagem})