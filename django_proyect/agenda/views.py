
import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contacto


def contactos_view(request):
    contacto_editar = None
    errores = []

    id_a_editar = request.GET.get('editar')
    if id_a_editar:
        contacto_editar = get_object_or_404(Contacto, id=id_a_editar)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        contacto_id = request.POST.get('contacto_id')

        if not nombre or not correo or not telefono:
            errores.append('Todos los campos son obligatorios.')

        patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if correo and not re.match(patron_correo, correo):
            errores.append('El correo electrónico no tiene un formato válido.')

        if telefono and not telefono.isdigit():
            errores.append('El teléfono solo debe contener números.')

        if not errores:
            if contacto_id:
                contacto = get_object_or_404(Contacto, id=contacto_id)
                contacto.nombre = nombre
                contacto.correo = correo
                contacto.telefono = telefono
                contacto.save()
            else:
                Contacto.objects.create(nombre=nombre, correo=correo, telefono=telefono)
            return redirect('contactos')
        else:
            if contacto_id:
                contacto_editar = get_object_or_404(Contacto, id=contacto_id)

    busqueda = request.GET.get('q', '')
    resultados_busqueda = None
    if busqueda:
        resultados_busqueda = Contacto.objects.filter(nombre__icontains=busqueda)

    contactos = Contacto.objects.all()

    return render(request, 'agenda/contactos.html', {
        'contactos': contactos,
        'resultados_busqueda': resultados_busqueda,
        'contacto_editar': contacto_editar,
        'errores': errores,
        'busqueda': busqueda,
    })

def eliminar_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    contacto.delete()
    return redirect('contactos')
