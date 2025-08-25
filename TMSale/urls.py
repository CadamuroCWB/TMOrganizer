from django.contrib import admin

from .views import contact
from django.urls import path, include

urlpatterns = [
    # CRUD contact
    path('contacts/', contact_list, name='contact_list'),
    path('contacts/create/', contact_create, name='contact_create'),
    path('contacts/<int:pk>/edit/', contact_update, name='contact_update'),
    path('contacts/<int:pk>/delete/', contact_delete, name='contact_delete'),
    # end CRUD contact
]
