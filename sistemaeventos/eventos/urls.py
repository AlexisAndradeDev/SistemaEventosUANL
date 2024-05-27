from django.urls import path
from . import views

urlpatterns = [
    path('', views.eventos, name='eventos'),
    path('<int:evento_id>/', views.evento_detalle, name='evento_detalle'),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('asistir/<int:evento_id>/', views.asistir_evento, name='asistir_evento'),
    path('editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
]