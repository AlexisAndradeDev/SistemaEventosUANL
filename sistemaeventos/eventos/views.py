from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from datetime import datetime

# Helper function to execute raw SQL queries
def execute_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description:
            return cursor.fetchall()
        else:
            return None

def eventos(request):
    query = "SELECT * FROM Eventos WHERE 1=1"
    params = []

    mes = request.GET.get('mes')
    if mes:
        query += " AND MONTH(fecha) = %s"
        params.append(mes)

    categoria = request.GET.get('categoria')
    if categoria:
        query += " AND categoria_id = %s"
        params.append(categoria)

    keyword = request.GET.get('keyword')
    if keyword:
        query += " AND nombre LIKE %s"
        params.append(f'%{keyword}%')

    eventos = execute_sql(query, params)
    categorias = execute_sql("SELECT id, nombre FROM Categoria")
    meses = (
        {'id': 1, 'nombre': 'Enero'},
        {'id': 2, 'nombre': 'Febrero'},
        {'id': 3, 'nombre': 'Marzo'},
        {'id': 4, 'nombre': 'Abril'},
        {'id': 5, 'nombre': 'Mayo'},
        {'id': 6, 'nombre': 'Junio'},
        {'id': 7, 'nombre': 'Julio'},
        {'id': 8, 'nombre': 'Agosto'},
        {'id': 9, 'nombre': 'Septiembre'},
        {'id': 10, 'nombre': 'Octubre'},
        {'id': 11, 'nombre': 'Noviembre'},
        {'id': 12, 'nombre': 'Diciembre'},  
    )

    return render(request, 'eventos/eventos.html', {'eventos': eventos, 'meses': meses, 'categorias': categorias})

def evento_detalle(request, evento_id):
    evento = execute_sql("SELECT e.id, e.nombre, e.descripcion, e.lugar, e.fecha, c.nombre as categoria, u.email as creador, e.creador_id FROM Eventos e JOIN Categoria c ON e.categoria_id = c.id JOIN Usuario u ON e.creador_id = u.id WHERE e.id = %s", [evento_id])
    asistentes = execute_sql("SELECT u.email FROM Asistentes a JOIN Usuario u ON a.usuario_id = u.id WHERE a.evento_id = %s", [evento_id])
    es_creador = 'user_id' in request.session and request.session['user_id'] == evento[0][7]
    return render(request, 'eventos/evento_detalle.html', {'evento': evento[0], 'asistentes': asistentes, 'es_creador': es_creador})

def crear_evento(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        lugar = request.POST.get('lugar')
        fecha_str = request.POST.get('fecha')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')  # Convertir string a datetime
        categoria_id = request.POST.get('categoria_id')
        creador_id = request.session['user_id']
        
        execute_sql(
            "INSERT INTO Eventos (nombre, descripcion, lugar, fecha, categoria_id, creador_id) VALUES (%s, %s, %s, %s, %s, %s)",
            [nombre, descripcion, lugar, fecha, categoria_id, creador_id]
        )
        
        messages.success(request, "Evento creado con éxito")
        return redirect('eventos')
    
    categorias = execute_sql("SELECT id, nombre FROM Categoria")
    return render(request, 'eventos/crear_evento.html', {'categorias': categorias})

def asistir_evento(request, evento_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    usuario_id = request.session['user_id']
    execute_sql("INSERT INTO Asistentes (evento_id, usuario_id) VALUES (%s, %s)", [evento_id, usuario_id])
    messages.success(request, "Te has registrado como asistente al evento")
    return redirect('evento_detalle', evento_id=evento_id)

def editar_evento(request, evento_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    evento = execute_sql("SELECT * FROM Eventos WHERE id = %s", [evento_id])
    if not evento or evento[0][5] != request.session['user_id']:
        messages.error(request, "No tienes permiso para editar este evento.")
        return redirect('eventos')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        lugar = request.POST.get('lugar')
        fecha_str = request.POST.get('fecha')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')  # Convertir string a datetime
        categoria_id = request.POST.get('categoria_id')
        
        execute_sql(
            "UPDATE Eventos SET nombre = %s, descripcion = %s, lugar = %s, fecha = %s, categoria_id = %s WHERE id = %s",
            [nombre, descripcion, lugar, fecha, categoria_id, evento_id]
        )
        
        messages.success(request, "Evento actualizado con éxito")
        return redirect('evento_detalle', evento_id=evento_id)
    
    categorias = execute_sql("SELECT id, nombre FROM Categoria")
    return render(request, 'eventos/editar_evento.html', {'evento': evento[0], 'categorias': categorias})