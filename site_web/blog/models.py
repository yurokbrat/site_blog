from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from uuid import uuid4


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="заголовок")
    content = models.TextField(verbose_name="контент")
    data_posted = models.DateTimeField(
        default=timezone.now, verbose_name="дата публикации"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    text = models.TextField(verbose_name="текст")
    created = models.DateTimeField(auto_now_add=True, verbose_name="создано в")
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return f"Comment by {self.author.username} to {self.post.title}"
