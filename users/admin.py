from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка юзера"""
    list_display = ('id', 'email', 'phone',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_date', 'course', 'payment_link', 'payment_id', 'summ')
