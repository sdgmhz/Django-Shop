from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm



class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    pass