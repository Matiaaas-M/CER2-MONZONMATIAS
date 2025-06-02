from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En ruta'),
        ('completada', 'Completada'),
    ]

    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    comentario_operario = models.TextField(blank=True, null=True)
    operario_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones')

    def __str__(self):
        return f"{self.ciudadano.username} - {self.material.nombre} ({self.estado})"