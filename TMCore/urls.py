from django.contrib import admin

from .views import about, contactus, index, custom_404_view, custom_500_view
from django.urls import path, include

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contactus/', contactus, name='contactus'),
    path('account/', include('django.contrib.auth.urls')),
]