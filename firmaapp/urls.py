from django.urls import path
from firmaapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.formulario_view, name='formulario'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('ver-pdf/<str:filename>/', views.ver_pdf, name='ver_pdf'),]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)