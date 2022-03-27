from django.contrib import admin

from .models import *


class WomenAdmin(admin.ModelAdmin):  # Наследуется от базового
    # Содержит список тех полей, которые мы пропишем
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}  # Заполнять автоамтически поле слаг на основании поля имя


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # Обязательно передаём кортеж используя (,)
    prepopulated_fields = {"slug": ("name",)}  # Заполнять автоамтически поле слаг на основании поля имя


# Зарегистрируем этот класс в функции register:
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
