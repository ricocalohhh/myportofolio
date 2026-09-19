from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm, ExperienceForm

from main.models import Experience, Education, Project


def show_main(request):
    context = {
        "name": "Enrico Oscar Harits Caloh",
        "npm": "2506539990",
        "study_program": "S1 Sistem Informasi",
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

def show_experience(request):
    experience_list = Experience.objects.all().order_by('-started_at')
    context = {
        'experience_list': experience_list
    }
    return render(request, 'experience.html', context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "form": form,
    }
    return render(request, "experience_form.html", context)

def show_projects(request):
    project_list = Project.objects.all()
    context = {
        'project_list': project_list
    }
    return render(request, 'projects.html', context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "form": form,
    }
    return render(request, "create_project.html", context)

def show_education(request):
    context = {
        'name': 'Enrico Oscar Harits Caloh',
        'npm': '2506539990',
        'study_program': 'S1 Sistem Informasi',
        'bio': 'Student in Information Systems with a strong focus on Finance, Business Development, Project Management, Product Management and Information Systems.',
        'education_list': Education.objects.all().order_by('-id')
    }
    
    return render(request, "education.html", context)

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
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Enrico Oscar Harits Caloh",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")