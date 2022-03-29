from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    # related_nmae используется для альтернативного связанного запроса вместо c.women_set.all() - на c.get_posts.all()
    # related_name='get_posts' - отключаем метод, чтобы не ломался сайт
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        # Сортировку записей по дате их создания и по заголовку с помощью еще одного атрибута ordering.
        # Необходимо закоммениторать для корректной работы - Women.objects.values('cat_id').annotate(Count('id'))
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('category', kwargs={'cat_id': self.pk})
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        # verbose_name – это специальный атрибут, отвечающий за название модели.
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']  # Если сортировка будет отключена, то будут возникать предупреждения
