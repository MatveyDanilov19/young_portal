from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('', views.rating_dashboard, name='dashboard'),    # Главная страница рейтинга
    path('upload/', views.upload_document, name='upload'), # Загрузка документа для баллов
]
