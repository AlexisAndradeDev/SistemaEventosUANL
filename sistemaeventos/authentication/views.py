from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection

def execute_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        else:
            return None

def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = execute_sql("SELECT * FROM Usuario WHERE email = %s", [email])
        
        if not user:
            messages.error(request, 'Correo electrónico inválido')
            return redirect('/login/')
        
        user = execute_sql("SELECT * FROM Usuario WHERE email = %s AND password = %s", [email, password])
        
        if not user:
            messages.error(request, "Contraseña inválida")
            return redirect('/login/')
        else:
            # Autenticación manual ya que no estamos utilizando el modelo de Django
            request.session['user_id'] = user[0][0]
            return redirect('/home/')
    
    return render(request, 'authentication/login.html')

def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        password = request.POST.get('password')
        
        user = execute_sql("SELECT * FROM Usuario WHERE email = %s", [email])
        
        if user:
            messages.info(request, "El correo electrónico ya está registrado.")
            return redirect('/register/')
        
        execute_sql(
            "INSERT INTO Usuario (email, apellido_paterno, apellido_materno, password) VALUES (%s, %s, %s, %s)",
            [email, apellido_paterno, apellido_materno, password]
        )
        
        messages.info(request, "Cuenta creada con éxito")
        return redirect(reverse('login'))
    
    return render(request, 'authentication/register.html')

def user_logout(request):
    logout(request)
    return redirect('login')