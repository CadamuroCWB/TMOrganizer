from django.contrib import admin

from .views import item
from django.urls import path, include

urlpatterns = [
    path('item/', item, name='item'),
]