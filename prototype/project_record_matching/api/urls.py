from django.urls import path
from project_record_matching.api import views

urlpatterns = [
    path('datasets/', views.dataset_list),
]
