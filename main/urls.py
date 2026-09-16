from django.urls import path

from main.views import show_main, show_experience, show_education, create_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path('education/', show_education, name='show_education'),
    path("projects/add/", create_project, name="create_project"),
]