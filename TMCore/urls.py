from django.contrib import admin
from rest_framework.routers import DefaultRouter
from datetime import date

from TMItem import views

from .views import IndexView, about
from .views import calendar, event_create, contactus
from .views import custom_404_view, custom_500_view
from .views import company_list, company_create, company_update, company_delete, opening_hours
from .views_naturalperson import naturalperson_list, naturalperson_create, naturalperson_update, naturalperson_delete

from django.urls import path, include

router = DefaultRouter()

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('404/', custom_404_view, name='custom_404'),
    path('500/', custom_500_view, name='custom_500'),
    path('about/', about, name='about'),
    path('account/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('calendar/<int:week_number>/<int:year>/', calendar, name='calendar'),
    path('event/create/', event_create, name='event_create'),
    path('opening-hours/', opening_hours, name='opening_hours'),
    # CRUD company
    path('companies/', company_list, name='company_list'),
    path('companies/create/', company_create, name='company_create'),
    path('companies/<int:pk>/edit/', company_update, name='company_update'),
    path('companies/<int:pk>/delete/', company_delete, name='company_delete'),
    # end CRUD company
    path('contactus/', contactus, name='contactus'),
    # CRUD NaturalPerson
    path('naturalpersons/', naturalperson_list, name='naturalperson_list'),
    path('naturalpersons/create/', naturalperson_create, name='naturalperson_create'),
    path('naturalpersons/<int:pk>/edit/', naturalperson_update, name='naturalperson_update'),
    path('naturalpersons/<int:pk>/delete/', naturalperson_delete, name='naturalperson_delete'),
]