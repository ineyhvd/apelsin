from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from user.forms import LoginForm, RegisterForm


# Create your views here.

#
# def login_page(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('shop:products')
#             else:
#                 messages.add_message(request,
#                                      messages.ERROR,
#                                      'Invalid login')
#     context = {
#         'form': form
#     }
#     return render(request, 'user/login.html', context=context)

class LoginPageView(View):
    form_class = LoginForm
    template_name = 'login.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['form']=self.form_class
        return context




def logout_page(request):
    logout(request)
    return redirect('shop:products')





class RegistrationPageView(View):
    form_class = RegisterForm
    template_name = 'user/register.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['form']=self.form_class
        return context