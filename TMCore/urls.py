from django.contrib import admin
from rest_framework.routers import DefaultRouter

from .views import about, contactus, index, custom_404_view, custom_500_view, company_list, company_create, company_update, company_delete
from django.urls import path, include

router = DefaultRouter()

urlpatterns = [
    path('', index, name='index'),
    path('404/', custom_404_view, name='custom_404'),
    path('500/', custom_500_view, name='custom_500'),
    path('about/', about, name='about'),
    path('api/', include(router.urls)),
    # CRUD company
    path('companies/', company_list, name='company_list'),
    path('companies/create/', company_create, name='company_create'),
    path('companies/<int:pk>/edit/', company_update, name='company_update'),
    path('companies/<int:pk>/delete/', company_delete, name='company_delete'),
    # end CRUD company
    path('contactus/', contactus, name='contactus'),
    path('account/', include('django.contrib.auth.urls')),
]