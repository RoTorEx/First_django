from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .utils import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class WomenHome(DataMixin, ListView):  # Класс представления
    '''Заменили функцию index на класс представления'''
    model = Women  # Атрибут ссылается на модель, выбирает все записи из табоицы и пытается отобразить в виде списка
    template_name = 'women/index.html'
    context_object_name = 'posts'

    # Новая версия на основе миксинов
    def get_context_data(self, *, object_list=None, **kwargs):  # Функция для динамических значений
        context = super().get_context_data(**kwargs)  # Распаковка словаря, теперь в context можно прописывать атрибуты
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        '''Два словаря c_def и contex будут формировать нужный контекст'''
        return context

    def get_queryset(self):  # Метод будет показывать, только опубликованные статьи на сайте
        return Women.objects.filter(is_published=True)


# Для функций-представления следует использовать декоратор, чтобы запретить неавторизованным пользователям "О сайте"
@login_required
def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


# LoginRequiredMixin - отвечает за логин пользователей
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  # Класс формы, который свазян с формой представления
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # функция reverse пытается сразу псотрить нужный маршрут в момент создания
    # экземпляра класса. А функция reverse_lazy будет создавать маршрут ьтолько когда она понадобится, возможно всегда
    # использовать эту функцию для безопасного построения маршрута
    # login_url = '/admin/'  # Адрес перенапрвления для незарегистрированных пользователей
    # указывать адрес напрямую не лучше практика, так что сделаем так:
    login_url = reverse_lazy('home')  # Адрес перенапрвления для незарегистрированных пользователей через функцию
    raise_exception = True  # Генерация исключения 403 - доступ запрещён

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    '''Класс представления для категорий'''
    model = Women  # Указываем модель
    template_name = 'women/index.html'  # Связываем с моделью
    context_object_name = 'posts'
    allow_empty = False  # False означает, что будет генерироваться 404, если передан несуществующий атрибут в списке

    def get_queryset(self):
        # Выберем только те категории, которые указаны в слаге, через kwargs получим словарь и через self берём словарь
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        # Формируем контекст данных, которые уже сформированы базовым классом
        context = super().get_context_data(**kwargs)
        # Берём первую запись из posts, и обращаемся к объекут, который берёт название
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                            cat_selected=context['posts'][0].cat_id)

        return dict(list(context.items()) + list(c_def.items()))
