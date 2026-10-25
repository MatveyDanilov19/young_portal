from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('create/', views.news_create, name='news_create'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
]
