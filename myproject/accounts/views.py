from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

class SignInView(AuthLoginView):
    authentication_form = AuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return super().get_success_url()
 
class SignOutView(AuthLogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL