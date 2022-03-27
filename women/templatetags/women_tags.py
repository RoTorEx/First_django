from django import template
from women.models import *

register = template.Library()


@register.simple_tag(name='getcats')  # Используется для превращения функции в тег
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()  # Обращение к БД и выборка из таблицы Категории всех записей
    else:
        return Category.objects.filter(pk=filter)  # Выборка будет по главному ключу


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}
