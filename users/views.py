import random

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Подтверждение',
                message=f'Код верификации: {new_user.confirm_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


class VerificationTemplateView(TemplateView):
    template_name = 'users/ver_email.html'

    def post(self, request):
        confirm_code = request.POST.get('confirm_code')
        user_code = User.objects.filter(confirm_code=confirm_code).first()

        if user_code is not None and user_code.confirm_code == confirm_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:register')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_pass(request):
    new_pass = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    send_mail(
        subject='Пароль успешно изменен',
        message=f'Новый пароль {new_pass}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_pass)
    request.user.save()
    return redirect(reverse('catalog:index'))
