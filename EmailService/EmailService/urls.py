from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('SendEmail/', include('SendEmail.urls')),
    path('EmailService/', include('django.contrib.auth.urls')),
    path('', include('SendEmail.urls')),
]
