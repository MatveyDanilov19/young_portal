from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Расширение пользователя: признак молодого специалиста и данные для справочника"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_young_specialist = models.BooleanField("Молодой специалист", default=True)
    university = models.CharField("Вуз", max_length=255, blank=True)
    course = models.PositiveSmallIntegerField("Курс", null=True, blank=True)
    skills = models.TextField("Навыки", blank=True)
    role_in_mc = models.CharField("Роль в Совете МС", max_length=100, blank=True, help_text="Например: Председатель, Член совета")

    class Meta:
        verbose_name = "Профиль специалиста"
        verbose_name_plural = "Профили специалистов"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
