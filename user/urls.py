from django.urls import path, include
from user import views

app_name = 'user'

urlpatterns = [
    path('login-oauth-page/', views.LoginPageView.as_view, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.RegistrationPageView.as_view(), name='register_page')
]
