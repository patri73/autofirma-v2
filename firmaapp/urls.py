from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_view, name='formulario'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('ver_pdf/<str:filename>/', views.ver_pdf, name='ver_pdf'),
    path('eliminar_pdf/<str:filename>/', views.eliminar_pdf, name='eliminar_pdf'),
]
