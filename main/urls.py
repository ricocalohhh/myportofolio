from django.urls import path

from main.views import show_main, show_experience, show_education, create_project, show_projects, get_projects_json, delete_project, create_experience, edit_experience, delete_experience, get_experience_json
from main.views import register, login_user, logout_user, toggle_star, toggle_star_experience, create_project_ajax, get_education_json, create_education, edit_education, delete_education
app_name = "main"

urlpatterns = [
    # Main & General
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    # Experience
    path("experience/", show_experience, name="show_experience"),
    path("experience/json/", get_experience_json, name="get_experience_json"), 
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:id>/edit/", edit_experience, name="edit_experience"),
    path("experience/<uuid:id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),

    # Projects
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),

    # Education
    # Education
    path("education/", show_education, name="show_education"),
    path("education/json/", get_education_json, name="get_education_json"),
    path("education/add/", create_education, name="create_education"),
    path("education/<int:id>/edit/", edit_education, name="edit_education"),      # Ubah ke <uuid:id> jika primary key model kamu UUID
    path("education/<int:id>/delete/", delete_education, name="delete_education"),  # Ubah ke <uuid:id> jika primary key model kamu UUID
]