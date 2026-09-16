from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm  

from django.shortcuts import render

from main.models import Experience, Education, Project


def show_main(request):
    context = {
        "name": "Enrico Oscar Harits Caloh",
        "npm": "2506539990",
        "study_program": "S1 Sisttem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada proses bisnis dan teknologi."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Enrico Oscar Harits Caloh",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        'name': 'Enrico Oscar Harits Caloh',
        'npm': '2506539990',
        'study_program': 'S1 Sistem Informasi',
        'bio': 'Student in Information Systems with a strong focus on Finance, Business Development, Project Management, Product Management and Information Systems.',
        'education_list': Education.objects.all().order_by('-id')
    }
    
    return render(request, "education.html", context)

def show_project(request):
    context = {
        'name': 'Enrico Oscar Harits Caloh',
        'education_list': Education.objects.all(),
    }
    
    return render(request, "projects.education.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Enrico Oscar Harits Caloh",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    context = {
        "name": "Enrico Oscar Harits Caloh",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)