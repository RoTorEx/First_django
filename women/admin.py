from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):  # Наследуется от базового
    # Содержит список тех полей, которые мы пропишем
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}  # Заполнять автоамтически поле слаг на основании поля имя
    # Содержит порядок и список редактируемых полей
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # Поля только для чтения
    save_on_top = True  # Отвечает за закрепление панельки редактирования

    def get_html_photo(self, object):  # Метод в админке будт показывать миниатюру изображения
        if object.photo:  # Проверка на наличие фото у постов
            # object будет ссылаться на текущую запись списка объекта модели women
            return mark_safe(f"<img src='{object.photo.url}' width=100>")  # mark_safe говорит НЕ экранировать html теги
        else:
            return "Нет фото"
    get_html_photo.short_description = "Миниатюра"  # Переименование поля в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # Обязательно передаём кортеж используя (,)
    prepopulated_fields = {"slug": ("name",)}  # Заполнять автоамтически поле слаг на основании поля имя


# Зарегистрируем этот класс в функции register:
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

# Переопределение названий в админ-панели
admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах'
