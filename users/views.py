from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import AuthForms, UserChangeProfile, UserRegisterForm
from users.models import EmailVerification, User


class UserRegistrationView(
    CreateView,
    SuccessMessageMixin,
):

    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'You\'re successfully register'
    form_class = UserRegisterForm
    model = User
    extra_context = {'title': 'Registration'}


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthForms


class UserProfileView(
    UpdateView,
    PermissionRequiredMixin,
):

    template_name = 'users/profile.html'
    model = User
    extra_context = {'title': 'User profile'}
    form_class = UserChangeProfile

    def has_permission(self):
        return self.request.user.pk == self.get_object().pk

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('users:login')

        if not self.has_permission():
            return redirect('main')

        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TemplateView):

    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):

        user = User.objects.get(email=kwargs.get('email'))
        code = kwargs.get('code')
        email_ver_object = EmailVerification.objects.filter(
            user=user, code=code,
        )

        if email_ver_object.exists() and \
                not email_ver_object.last().is_expired():

            user.is_verified_email = True
            user.save()
            email_ver_object.delete()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('main')
