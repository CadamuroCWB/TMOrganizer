from .views import item
from django.urls import path

urlpatterns = [
    path('item/', item, name='item'),
]