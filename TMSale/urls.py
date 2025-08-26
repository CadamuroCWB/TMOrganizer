from django.contrib import admin

from .views import contact_list, contact_create, contact_update, contact_delete
from django.urls import path, include

urlpatterns = [
    # CRUD contact
    path('contacts/', contact_list, name='contact_list'),
    path('contacts/create/', contact_create, name='contact_create'),
    path('contacts/<int:pk>/edit/', contact_update, name='contact_form'),
    path('contacts/<int:pk>/delete/', contact_delete, name='contact_confirm_delete'),
    # end CRUD contact
]

