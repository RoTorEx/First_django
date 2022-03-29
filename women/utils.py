from django.db.models import Count
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# class DataMixin:
#     '''Метод и класс будет формировать нужный контекст по умолчанию.
#     Избавляемся от дублирования кода к классах WomenHome, AddPage, ShowPost, WomenCategory'''
#     def get_user_context(self, **kwargs):
#         context = kwargs
#         cats = Category.objects.all()  # Список категорий
#         context['menu'] = menu
#         context['cats'] = cats
#         if 'cat_selected' not in context:  # Проверка, если ключ определяем, то он будет присутствовать
#             context['cat_selected'] = 0  # Ключ
#         return context


class DataMixin:
    '''Переработаем класс, чтобы добавить статью видел только авторизированный пользователь'''
    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()  # Список категорий
        # используется агрегирующая функция, и которая считает кол-во постов связанное с этой рубрикой
        cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()  # Копия словаря сохраняется
        # Если пользователь не авторизован, смотри это через объект request. У которого есть объект user,
        # у которого есть свойство, которое принимает True или False
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu  # В контекст передаётся ссылка на меню
        context['cats'] = cats
        if 'cat_selected' not in context:  # Проверка, если ключ определяем, то он будет присутствовать
            context['cat_selected'] = 0  # Ключ

        return context
