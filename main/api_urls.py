from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    path("experience/", api_views.experience_list_api, name="experience-list"),
    path("experience/<uuid:experience_id>/", api_views.experience_detail_api, name="experience-detail"),
    path("experience/<uuid:experience_id>/star/", api_views.experience_star_api, name="experience-star"),
]