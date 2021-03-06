from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:

    '''Переработаем класс, чтобы добавить статью видел только авторизированный пользователь'''

    paginate_by = 3  # Количетво постов на одной странице

    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()  # Список категорий
        # используется агрегирующая функция, и которая считает кол-во постов связанное с этой рубрикой
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('women'))
            cache.set('cats', cats, 60)

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
