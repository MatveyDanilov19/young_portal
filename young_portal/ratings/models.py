from django.db import models
from django.contrib.auth.models import User


class DocumentSubmission(models.Model):
    """Загрузка документов для получения баллов (Пункт 5 ТЗ)"""
    TYPE_CHOICES = [
        ('cert', 'Сертификат'),
        ('diploma', 'Диплом'),
        ('letter', 'Рекомендательное письмо'),
        ('other', 'Другое'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    document_type = models.CharField("Тип документа", max_length=20, choices=TYPE_CHOICES)
    file_path = models.FileField("Файл", upload_to='documents/')
    score_value = models.IntegerField("Начисленные баллы", default=0)
    status = models.CharField("Статус проверки", max_length=20, default='pending') # pending, approved, rejected
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)

    class Meta:
        verbose_name = "Загруженный документ"
        verbose_name_plural = "Загруженные документы"

    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"


class UserRating(models.Model):
    """Агрегация рейтинга пользователя (Пункт 6 ТЗ)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rating')
    total_score = models.IntegerField("Итоговый рейтинг", default=0)
    last_updated = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Рейтинг пользователя"
        verbose_name_plural = "Рейтинги пользователей"

    def __str__(self):
        return f"{self.user.username}: {self.total_score} баллов"
