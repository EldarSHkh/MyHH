from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from app_vacancies.form import MyUserCreationForm


class UserSignupView(CreateView):
    form_class = MyUserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
