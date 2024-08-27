from django.urls import path

from content_app.apps import ContentAppConfig
from content_app.views import index

app_name = ContentAppConfig.name

urlpatterns = [
    path('', index, name='index'),
]
