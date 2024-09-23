import math
import secrets
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:phone_confirm')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        digits = [i for i in range(0, 10)]
        code_confirm = ""
        for i in range(6):
            ind_x = math.floor(random.random() * 10)
            code_confirm += str(digits[ind_x])
        print(code_confirm)
        user.code_confirm = code_confirm
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/code_confirm/{user.pk}/'
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def phone_confirm(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('phone') and request.POST.get('code_confirm'):
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            code_confirm = request.POST.get('code_confirm')
            if User.objects.filter(email=email, phone=phone, code_confirm=code_confirm).exists():
                user = get_object_or_404(User, email=email, phone=phone, code_confirm=code_confirm)
                user.is_active = True
                user.save()
                return redirect('users:login')
            else:
                context = {'mistake': "Введенная информация не верна!"}
        else:
            context = {'mistake': "Заполните все поля!"}
    return render(request, 'users/phone_confirm.html', context)
