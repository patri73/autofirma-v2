from django import forms
from django.core.exceptions import ValidationError
import re

# Validadores
def validar_nombre_apellido(value):
    caracteres_no_validos = ['|', '!', '¡', '#', '$', '/', '\\', '(', ')', '=', '?',
                             '¿', '^', '*', '+', '-', '_', ';', '[', ']', '{', '}',
                             '<', '>', '¬', '@', '"', "'"]
    
    for char in caracteres_no_validos:
        if char in value:
            raise ValidationError(f'El campo no puede contener el carácter: {char}')
    
    if any(char.isdigit() for char in value):
        raise ValidationError('El campo no puede contener números.')

def validar_dni(value):
    caracteres_no_validos = ['|', '!', '¡', '#', '$', '/', '\\', '(', ')', '=', '?',
                             '¿', '^', '*', '+', '-', '_', ';', '[', ']', '{', '}',
                             '<', '>', '¬', '@', '"', "'"]

    for char in caracteres_no_validos:
        if char in value:
            raise ValidationError(f'El DNI no puede contener el carácter: {char}')

    patron_dni = re.compile(r'^\d{8}[A-Za-z]$')
    if not patron_dni.match(value):
        raise ValidationError(
            'Introduce un DNI válido, 8 números seguidos de una letra (ejemplo: 12345678A).',
            params={'value': value},
        )
    

def validar_texto_libre(value):
    if '/' in value:
    
        raise ValidationError(
            "El texto no puede contener el carácter '/'.",
            params={'value': value},
        )

class FirmaForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre *',
        max_length=100,
        validators=[validar_nombre_apellido],
        error_messages={
            'required': 'Este campo es obligatorio',
            'max_length': 'El nombre no puede tener más de 100 caracteres'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )

    apellido1 = forms.CharField(
        label='Primer apellido *',
        max_length=100,
        validators=[validar_nombre_apellido],
        error_messages={
            'required': 'Este campo es obligatorio',
            'max_length': 'El primer apellido no puede tener más de 100 caracteres'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer apellido'})
    )

    apellido2 = forms.CharField(
        label='Segundo apellido',
        max_length=100,
        validators=[validar_nombre_apellido],
        required=False,
        error_messages={
            'max_length': 'El segundo apellido no puede tener más de 100 caracteres'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo apellido'})
    )

    dni = forms.CharField(
        label='DNI *',
        max_length=9,
        validators=[validar_dni],
        error_messages={
            'required': 'Este campo es obligatorio',
            'max_length': 'El DNI no puede tener más de 9 caracteres'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 12345678A'})
    )

    texto = forms.CharField(
        label='Texto libre',
        required=False,
        initial='',
        max_length=512,
        validators=[validar_texto_libre],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Máximo 512 caracteres',
            'oninput': 'actualizarContador()',
            'id': 'texto'
        })
    )
