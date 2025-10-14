from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    contact_list, contact_create, contact_update, contact_delete,
    ClientViewSet, ContactViewSet,
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView
)

# Router para ViewSets do Django REST Framework
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'contacts-api', ContactViewSet)

urlpatterns = [
    # CRUD contact (views tradicionais)
    path('contacts/', contact_list, name='contact_list'),
    path('contacts/create/', contact_create, name='contact_create'),
    path('contacts/<int:pk>/edit/', contact_update, name='contact_form'),
    path('contacts/<int:pk>/delete/', contact_delete, name='contact_confirm_delete'),
    
    # Class-Based Views para Client (alternativa elegante ao CRUD)
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<uuid:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<uuid:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<uuid:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    
    # API REST endpoints (ViewSets)
    path('api/', include(router.urls)),
]

