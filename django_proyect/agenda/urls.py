from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactos_view, name='contactos'),
    path('eliminar/<int:id>/', views.eliminar_contacto, name='eliminar_contacto'),
]