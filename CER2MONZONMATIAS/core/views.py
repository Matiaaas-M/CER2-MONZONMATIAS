from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Material, Solicitud
from django.contrib.auth.models import User
from django.db.models import Count, Avg
import datetime

def inicio(request):
    solicitudes_por_mes = Solicitud.objects.values('fecha_estimada__month').annotate(total=Count('id'))
    materiales_mas_comunes = Solicitud.objects.values('material__nombre').annotate(total=Count('id')).order_by('-total')[:5]
    tiempo_promedio = Solicitud.objects.exclude(estado='pendiente').aggregate(promedio=Avg('cantidad'))
    
    return render(request, 'core/inicio.html', {
        'solicitudes_por_mes': solicitudes_por_mes,
        'materiales_mas_comunes': materiales_mas_comunes,
        'tiempo_promedio': tiempo_promedio
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

@login_required
def nueva_solicitud(request):
    materiales = Material.objects.all()
    if request.method == 'POST':
        material_id = request.POST['material']
        cantidad = request.POST['cantidad']
        fecha = request.POST['fecha']
        material = Material.objects.get(id=material_id)
        Solicitud.objects.create(
            ciudadano=request.user,
            material=material,
            cantidad=cantidad,
            fecha_estimada=fecha
        )
        return redirect('historial')
    return render(request, 'core/nueva_solicitud.html', {'materiales': materiales})

@login_required
def historial(request):
    solicitudes = Solicitud.objects.filter(ciudadano=request.user)
    return render(request, 'core/historial.html', {'solicitudes': solicitudes})

def metricas(request):
    hoy = datetime.date.today()
    solicitudes_por_mes = Solicitud.objects.values('fecha_estimada__month').annotate(total=Count('id'))
    materiales_mas_comunes = Solicitud.objects.values('material__nombre').annotate(total=Count('id')).order_by('-total')[:5]
    tiempo_promedio = Solicitud.objects.exclude(estado='pendiente').aggregate(promedio=Avg('cantidad'))
    return render(request, 'core/metricas.html', {
        'solicitudes_por_mes': solicitudes_por_mes,
        'materiales_mas_comunes': materiales_mas_comunes,
        'tiempo_promedio': tiempo_promedio
    })