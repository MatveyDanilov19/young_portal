from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_list, name='profile_list'),      # Справочник всех членов МС
    path('<int:pk>/', views.profile_detail, name='profile_detail'), # Детальная страница
    path('edit/', views.profile_edit, name='profile_edit'),      # Редактирование своего профиля
    path('dashboard/', views.dashboard, name='dashboard'),
]
