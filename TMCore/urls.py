from django.contrib import admin

from .views import about, contactus, index, custom_404_view, custom_500_view
from django.urls import path, include

urlpatterns = [
    path('', index, name='index'),
    path('404/', custom_404_view, name='custom_404'),
    path('500/', custom_500_view, name='custom_500'),
    path('about/', about, name='about'),
    path('contactus/', contactus, name='contactus'),
    path('account/', include('django.contrib.auth.urls')),
]