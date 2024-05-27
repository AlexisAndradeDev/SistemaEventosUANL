from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import connection

def execute_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description:
            return cursor.fetchall()
        else:
            return None

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = execute_sql("SELECT * FROM Usuario WHERE email = %s", [email])

        if not user:
            messages.error(request, 'Correo electrónico inválido')
            return redirect(reverse('login'))
        
        user = execute_sql("EXEC login_user @Email = %s, @Password = %s", [email, password])
        
        if not user:
            messages.error(request, "Contraseña inválida")
            return redirect(reverse('login'))
        else:
            # Autenticación manual ya que no estamos utilizando el modelo de Django
            request.session['user_id'] = user[0][0]
            return redirect('/eventos/')
    
    return render(request, 'authentication/login.html')

def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        password = request.POST.get('password')
        
        user = execute_sql("SELECT * FROM Usuario WHERE email = %s", [email])
        
        if user:
            messages.info(request, "El correo electrónico ya está registrado.")
            return redirect(reverse('register'))
        
        execute_sql(
            "EXEC register_user @Email=%s, @Nombre=%s, @ApellidoPaterno=%s, @ApellidoMaterno=%s, @Password=%s",
            [email, nombre, apellido_paterno, apellido_materno, password]
        )

        messages.info(request, "Cuenta creada con éxito")
        user_logout(request)
        return redirect(reverse('login'))
    
    return render(request, 'authentication/register.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def delete_account(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        user_id = request.session.get('user_id')
        execute_sql("EXEC delete_user @user_id=%s", [user_id])
        user_logout(request)
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
        return redirect('login')
    return render(request, 'authentication/delete_account.html')
