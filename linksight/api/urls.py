from django.urls import path
from linksight.api import views

urlpatterns = [
    path('users/<id>', views.user.user_detail),
    path('datasets/', views.dataset.dataset_list),
    path('datasets/<uuid:id>/preview', views.dataset.dataset_preview),
    path('datasets/<uuid:id>/match', views.dataset.dataset_match),
    path('matches/<uuid:id>/items', views.match.match_items),
    path('matches/<uuid:id>/save-choices', views.match.match_save_choices),
    path('matches/<uuid:id>/preview', views.match.match_preview),
]
