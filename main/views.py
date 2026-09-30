from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from main.forms import ProjectForm, ExperienceForm
from main.models import Experience, Education, Project
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied 

from datetime import datetime

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Enrico Oscar Harits Caloh",
                "npm": "2506539990",
                "study_program": "S1 Sistem Informasi",
                "bio": (
                    "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
                    "pada proses bisnis dan teknologi."
                ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


# ==================== EXPERIENCE SECTION ====================

def show_projects(request):
    context = {
        'name': request.user.username if request.user.is_authenticated else 'Visitor',
    }
    return render(request, "project.html", context) # Pastikan nama template sesuai, misal "projects.html" atau "project.html"

@login_required(login_url="/login/")
def create_project(request):
    # Hanya izinkan superuser
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "form": form,
    }
    return render(request, "create_project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        # Indentasi diperbaiki: Masuk ke dalam loop for
        data.append({
            "id": str(project.id),
            "title": project.title,
            "description": project.description,
            "tech_stack": project.tech_stack,
            "project_url": project.project_url,
            "project_image_url": project.project_image_url,
            "star_count": starred_users.count(),
            "is_starred": is_starred,
            "starred_by_names": starred_by_names,
        })

    return JsonResponse(data, safe=False)

@login_required
def delete_project(request, id):
    # Validasi Hak Akses: Hanya superuser yang boleh menghapus
    if not request.user.is_superuser:
        return JsonResponse({'message': 'Akses Ditolak: Anda tidak memiliki izin.'}, status=403)

    if request.method == 'POST':
        project = get_object_or_404(Project, pk=id)
        project.delete()
        return JsonResponse({'message': 'Proyek berhasil dihapus!'}, status=200)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
            is_starred = False
        else:
            project.starred_by.add(request.user)
            is_starred = True

        return JsonResponse({
            "message": "Status star berhasil diperbarui.",
            "is_starred": is_starred,
            "star_count": project.starred_by.count(),
        }, status=200)

    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)

@login_required(login_url="/login/")
@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# ==================== EXPERIENCE SECTION ====================

# --- READ (Dapat diakses oleh SIAPA PUN: Anonymous, User, Editor, Superuser) ---

def show_experience(request):
    context = {
        'name': request.user.username if request.user.is_authenticated else 'Visitor',
    }
    return render(request, "experience.html", context)

# --- CREATE (Hanya Superuser) ---
@login_required(login_url="/login/")
@require_POST
def create_experience(request):
    # Cek hak akses
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk menambah data."}, 
            status=403
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Berhasil menyimpan!"}, status=201)
    
    return JsonResponse(
        {
            "status": "error", 
            "message": "Gagal menyimpan, periksa kembali input Anda.",
            "errors": form.errors.get_json_data()
        }, 
        status=400
    )

# --- EDIT / UPDATE (Hanya Editor/is_staff ATAU Superuser) ---
@login_required(login_url="/login/")
@require_POST
def edit_experience(request, id):
    # 1. Hak Akses / Otorisasi Backend -> Status 403 (Forbidden)
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        return JsonResponse(
            {"status": "error", "message": "Anda tidak memiliki izin untuk mengedit data ini."}, 
            status=403
        )

    # 2. Ambil objek Experience atau return 404 jika tidak ditemukan
    try:
        experience = Experience.objects.get(pk=id)
    except Experience.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Data pengalaman tidak ditemukan."}, 
            status=404
        )

    # 3. Binding data request.POST ke ExperienceForm dengan instance yang ada
    form = ExperienceForm(request.POST, instance=experience)

    # 4. Validasi Form
    if form.is_valid():
        form.save()
        return JsonResponse(
            {"status": "success", "message": "Data pengalaman berhasil diperbarui!"}, 
            status=200 # Status 200 OK
        )
    else:
        # Jika input tidak valid (misal: format tanggal salah) -> Status 400 Bad Request
        return JsonResponse(
            {
                "status": "error", 
                "message": "Gagal memperbarui data. Periksa kembali input Anda.",
                "errors": form.errors.get_json_data()
            }, 
            status=400
        )

# --- DELETE (Hanya Superuser) ---
@login_required(login_url="/login/")
@require_POST
def delete_experience(request, id):
    if not request.user.is_superuser:
        return JsonResponse({"message": "Akses ditolak."}, status=403)

    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    return JsonResponse({"message": "Pengalaman berhasil dihapus!"}, status=200)

def get_experience_json(request):
    query = request.GET.get('q', '')
    experiences = Experience.objects.all()
    
    if query:
        experiences = experiences.filter(
            Q(title__icontains=query) | Q(category__icontains=query)
        )

    data = []
    for exp in experiences:
        data.append({
            'id': str(exp.id),
            'title': exp.title,
            'category': exp.category,  
            'description': exp.description,
            'started_at': exp.started_at.strftime('%Y-%m-%d') if exp.started_at else None,
            'ended_at': exp.ended_at.strftime('%Y-%m-%d') if exp.ended_at else None,
            'is_starred': exp.starred_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False,
            'star_count': exp.starred_by.count(),
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
@require_POST
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    star_relation = experience.stars if hasattr(experience, 'stars') else experience.starred_by
    
    if request.user in star_relation.all():
        star_relation.remove(request.user)
        is_starred = False
    else:
        star_relation.add(request.user)
        is_starred = True
        
    return JsonResponse({
        "message": "Status star berhasil diperbarui.",
        "is_starred": is_starred,
        "star_count": star_relation.count()
    }, status=200)

# ==================== EDUCATION SECTION ==================== 
def show_education(request):
    context = {
        'name': 'Enrico Oscar Harits Caloh',
        'npm': '2506539990',
        'study_program': 'S1 Sistem Informasi',
        'bio': 'Student in Information Systems with a strong focus on Finance, Business Development, Project Management, Product Management and Information Systems.',
    }
    return render(request, "education.html", context)

# Endpoint AJAX Get List Data JSON
def get_education_json(request):
    query = request.GET.get("q", "").strip()
    educations = Education.objects.all().order_by('-id')

    if query:
        educations = educations.filter(institution__icontains=query)

    data = [
        {
            "id": edu.id,
            "institution": edu.institution,
            "degree": edu.degree,
            "duration": edu.duration,
            "description": edu.description or "",
            "logo_url": edu.logo_url or "",
        }
        for edu in educations
    ]
    return JsonResponse(data, safe=False)

# Endpoint AJAX Create
@login_required
@require_POST
def create_education(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({"status": "error", "message": "Akses ditolak."}, status=403)

    institution = request.POST.get("institution", "").strip()
    degree = request.POST.get("degree", "").strip()
    duration = request.POST.get("duration", "").strip()
    description = request.POST.get("description", "").strip()
    logo_url = request.POST.get("logo_url", "").strip()

    if not (institution and degree and duration):
        return JsonResponse({"status": "error", "message": "Field wajib tidak boleh kosong."}, status=400)

    Education.objects.create(
        institution=institution,
        degree=degree,
        duration=duration,
        description=description,
        logo_url=logo_url,
    )
    return JsonResponse({"status": "success", "message": "Pendidikan berhasil ditambahkan!"}, status=201)

# Endpoint AJAX Edit
@login_required
@require_POST
def edit_education(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponseForbidden("Unauthorized")

    edu = get_object_or_404(Education, pk=id)
    edu.institution = request.POST.get("institution", edu.institution)
    edu.degree = request.POST.get("degree", edu.degree)
    edu.duration = request.POST.get("duration", edu.duration)
    edu.description = request.POST.get("description", edu.description)
    edu.logo_url = request.POST.get("logo_url", edu.logo_url)
    edu.save()

    return JsonResponse({"status": "success", "message": "Pendidikan berhasil diperbarui!"})

# Endpoint AJAX Delete
@login_required
@require_POST
def delete_education(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Unauthorized")

    edu = get_object_or_404(Education, pk=id)
    edu.delete()
    return JsonResponse({"status": "success", "message": "Pendidikan berhasil dihapus!"})


