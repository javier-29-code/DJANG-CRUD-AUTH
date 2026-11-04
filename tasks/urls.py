from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="iniciar_sesion"),
    path("logout/", views.cerrar_sesion, name="cerrar_sesion"),
    path("tasks/", views.tareas, name="tareas"),
    path("tasks/create/", views.crear_tarea, name="crear_tarea"),
    path(
    "tasks/<int:tarea_id>/",
    views.detalle_tarea,
    name="detalle_tarea",
    ),
    path(
    "tasks/<int:tarea_id>/complete/",
    views.completar_tarea,
    name="completar_tarea",
    ),
    path(
        "tasks/<int:tarea_id>/delete/",
        views.eliminar_tarea,
        name="eliminar_tarea",
    ),
    
    path(
        "tasks/completed/",
        views.tareas_completadas,
        name="tareas_completadas",
    ),
]