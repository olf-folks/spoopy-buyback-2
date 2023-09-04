from django.urls import path
from . import views

app_name = 'blueprint'  # Set the app_name

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.blueprint_list, name='blueprint_list'),
    path('<int:blueprint_id>/', views.blueprint_detail, name='blueprint_detail'),
]
