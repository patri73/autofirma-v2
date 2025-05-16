from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.conf import settings
from django.urls import reverse
from reportlab.pdfgen import canvas    
from .forms import FirmaForm
from reportlab.lib.pagesizes import A4
from django.conf import settings
import os
from datetime import datetime


def formulario_view(request):
    if request.method == 'POST':
        form = FirmaForm(request.POST)
        if form.is_valid():
            request.session['datos_formulario'] = form.cleaned_data
            return redirect('confirmacion')
    else:
        datos_guardados = request.session.get('datos_formulario')
        if datos_guardados:
            form = FirmaForm(initial=datos_guardados)
        else:
            form = FirmaForm()

    return render(request, 'firmaapp/formulario.html', {'form': form})


def confirmacion(request):
    datos = request.session.get('datos_formulario')
    if not datos:
        return redirect('formulario')  

    datos['apellidos'] = f"{datos.get('apellido1', '')} {datos.get('apellido2', '')}".strip()

    return render(request, 'firmaapp/confirmacion.html', {'datos_formulario': datos})


def generar_pdf(request):
    datos = request.session.get('datos_formulario')
    if not datos:
        return redirect('formulario')

    nombre = datos['nombre']
    apellido1 = datos['apellido1']
    apellido2 = datos.get('apellido2', '')
    texto = datos['texto']
    dni = datos['dni']
    fecha = datetime.now().strftime("%d/%m/%Y")

    apellidos = f"{apellido1} {apellido2}".strip()
    filename = f"{dni}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    logo_path = os.path.join(settings.BASE_DIR, 'firmaapp', 'TANGRAMBPM.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 40, height - 180, width=100, preserveAspectRatio=True)

    c.setFont("Helvetica", 12)
    y = height - 150
    c.drawString(40, y, f"Estimado/a {nombre} {apellidos},")
    y -= 30
    c.drawString(40, y, "A continuación, recogemos el texto de su solicitud:")
    y -= 40

    for linea in texto.splitlines():
        c.drawString(40, y, linea)
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 100

    y -= 30
    c.drawString(40, y, f"Dándole las gracias, atentamente, {fecha}")

    if os.path.exists(logo_path):
        c.drawImage(logo_path, 430, 40, width=100, preserveAspectRatio=True)

    c.save()

    ver_pdf_url = reverse('ver_pdf', kwargs={'filename': filename})

    return render(request, 'firmaapp/pdf_generado.html', {
        'datos': datos,
        'pdf_filename': filename,
        'ver_pdf_url': ver_pdf_url,
    })


def eliminar_pdf(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return redirect('formulario')
    else:
        raise Http404("PDF no encontrado")


def ver_pdf(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'), content_type='application/pdf')
        response["X-Frame-Options"] = "SAMEORIGIN"  
        return response
    else:
        raise Http404("PDF no encontrado")