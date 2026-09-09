from django.shortcuts import render

from main.models import Experience, Education 


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