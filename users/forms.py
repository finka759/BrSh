from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import BooleanField

from users.models import User, Payment


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("phone", "email", "password1", "password2")


class PaymentCreateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("course",)
