
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('nueva/', views.nueva_solicitud, name='nueva_solicitud'),
    path('historial/', views.historial, name='historial'),
    path('metricas/', views.metricas, name='metricas'),
]
