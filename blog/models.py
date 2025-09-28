from django.db import models


class Article(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название статьи",
        help_text="Введите название статьи",
    )

    content = models.TextField(
        verbose_name="Содержимое статьи",
        help_text="Введите содержимое статьи",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        verbose_name="Превью", help_text="Добавьте изображение", blank=True, null=True
    )

    created_at = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    published_status = models.BooleanField(
        default=False,
        verbose_name="Статус публикации",
        help_text="Укажите статус публикации",
    )

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at", "title"]

    def __str__(self):
        return f"{self.title}"
