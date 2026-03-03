from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError

from ..models.convidado_model import Convidado


class RegisterView(View):
    template_name = 'main/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # validação de campos vazios
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            return render(request, self.template_name)

        # validação de senhas iguais
        if password != password_confirm:
            messages.error(request, 'As senhas não correspondem.')
            return render(request, self.template_name)

        # validação de comprimento da senha
        if len(password) < 6:
            messages.error(request, 'A senha deve ter no mínimo 6 caracteres.')
            return render(request, self.template_name)

        # verificar se o usuário já existe
        if Convidado.objects.filter(username=username).exists():
            messages.error(request, 'Este usuário já está registrado.')
            return render(request, self.template_name)

        if Convidado.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está registrado.')
            return render(request, self.template_name)

        try:
            # criar novo convidado
            convidado = Convidado.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                telefone=telefone,
            )
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
            return render(request, self.template_name)


class LoginView(View):
    template_name = 'main/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Usuário e senha são obrigatórios.')
            return render(request, self.template_name)

        # autenticar o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return render(request, self.template_name)


@method_decorator(login_required(login_url='login'), name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Você foi desconectado.')
        return redirect('home')
