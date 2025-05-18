# artifacts/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('artifacts/', views.artifact_list, name='artifact_list'),
    path('new/', views.artifact_create, name='artifact_create'),
    path('<int:pk>/', views.artifact_detail, name='artifact_detail'),
    path('edit/<int:pk>/', views.artifact_update, name='artifact_update'),
    path('delete/<int:pk>/', views.artifact_delete, name='artifact_delete'),
    path('<int:artifact_id>/add_restoration/', views.add_restoration, name='add_restoration'),
    path('artifact/<int:artifact_id>/update_inventory/', views.update_inventory, name='update_inventory'),

]

