from django.urls import path
from linksight.api import views

urlpatterns = [
    path('datasets/', views.dataset_list),
    path('datasets/<uuid:id>/preview', views.dataset_preview),
    path('datasets/<uuid:id>/match', views.dataset_match),
    path('matches/<uuid:id>/items', views.match_items),
    path('matches/<uuid:id>/check', views.match_check),
]
