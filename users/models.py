from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="email",
        help_text="укажите ваш email",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        help_text="укажите ваш телефон",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        **NULLABLE,
    )
    token = models.CharField(
        max_length=100,
        verbose_name="Token",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.email}"


class Payment(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        verbose_name='пользователь'
    )
    payment_date = models.DateField(
        verbose_name='дата оплаты',
        **NULLABLE
    )
    course = models.ForeignKey(
        'content_app.Course',
        on_delete=models.CASCADE,
        verbose_name='оплаченный курс',
        **NULLABLE,
    )
    payment_link = models.URLField(
        max_length=400,
        verbose_name='ссылка для оплаты',
        **NULLABLE
    )
    payment_id = models.CharField(
        max_length=255,
        verbose_name='идентификатор платежа',
        **NULLABLE
    )
    summ = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="сумма платежа",
        default=0
    )

    def __str__(self):
        return f"{self.user}: ({self.course}, {self.summ} руб.)"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
