from django.urls import path
from linksight.api import views

urlpatterns = [
    path('datasets/', views.dataset_list),
]
