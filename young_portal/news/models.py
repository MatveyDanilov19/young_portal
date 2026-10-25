from django.db import models
from django.contrib.auth.models import User


class NewsPost(models.Model):
    PORTAL_SCOPE_CHOICES = [
        ('main', 'Основной портал'),
        ('mc', 'Портал МС'),
        ('both', 'Оба портала'),
    ]

    title = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Текст новости")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    portal_scope = models.CharField("Где публиковать", max_length=10, choices=PORTAL_SCOPE_CHOICES, default='main')
    image = models.ImageField("Фото", upload_to='news_images/', null=True, blank=True)  # <-- добавлено
    is_published = models.BooleanField("Опубликовано", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class NewsLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_likes')
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField("Дата лайка", auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class NewsComment(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Дата комментария", auto_now_add=True)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username}"

