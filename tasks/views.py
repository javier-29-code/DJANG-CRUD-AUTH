from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from .models import Task

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

def inicio(request):
    return render(request, "inicio.html")

from .forms import TaskForm, RegistroForm, InicioSesionForm

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("tareas")
    else:
        form = RegistroForm()

    return render(request, "signup.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = InicioSesionForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("tareas")
    else:
        form = InicioSesionForm(request)

    return render(request, "signin.html", {"form": form})


@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")

@login_required(login_url="iniciar_sesion")
def tareas(request):
    tareas_pendientes = Task.objects.filter(
        user=request.user,
        datecompleted__isnull=True,
    ).order_by("-created")

    return render(request, "tasks.html", {
        "tareas": tareas_pendientes,
    })
    
    
@login_required(login_url="iniciar_sesion")
def crear_tarea(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.user = request.user
            tarea.save()
            return redirect("tareas")
    else:
        form = TaskForm()

    return render(request, "create_task.html", {"form": form})

@login_required(login_url="iniciar_sesion")
def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=tarea)

        if form.is_valid():
            form.save()
            return redirect("tareas")
    else:
        form = TaskForm(instance=tarea)

    return render(request, "task_detail.html", {
        "tarea": tarea,
        "form": form,
    })


@login_required(login_url="iniciar_sesion")
@require_POST
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
    tarea.datecompleted = timezone.now()
    tarea.save()
    return redirect("tareas")


@login_required(login_url="iniciar_sesion")
@require_POST
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
    tarea.delete()
    return redirect("tareas")

@login_required(login_url="iniciar_sesion")
def tareas_completadas(request):
    completadas = Task.objects.filter(
        user=request.user,
        datecompleted__isnull=False,
    ).order_by("-datecompleted")

    return render(request, "tasks_completed.html", {
        "tareas": completadas,
    })