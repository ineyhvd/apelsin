from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views import View
from user.forms import LoginForm, RegisterForm
from django.conf import settings


class LoginPageView(View):
    form_class = LoginForm
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('shop:products')
            else:
                messages.error(request, 'Invalid login credentials.')
        return self.render_to_response({'form': form})


class RegistrationPageView(View):
    form_class = RegisterForm
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')

            subject = 'Welcome to Our Website!'
            message = f'Hi {user.username},\n\nThank you for registering on our website. We are excited to have you!'
            from_email = settings.EMAIL_HOST_USER  # Django settings faylida saqlangan email
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('user:login')  # Ro'yxatdan o'tgandan keyin login sahifasiga yo'naltirish
        return self.render_to_response({'form': form})


class LogoutPageView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('shop:products')  # Tizimdan chiqishdan so'ng shop sahifasiga yo'naltirish
