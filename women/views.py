from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .utils import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# В классe ListView уже представлена наследование к классу Paginator
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
        # return Women.objects.filter(is_published=True)  # Тут происходит выборка записей из таблицы Women
        # Совместно с этими данными будут загружены и данные из иаблицы категорий
        return Women.objects.filter(is_published=True).select_related('cat')


# Для функций-представления следует использовать декоратор, чтобы запретить неавторизованным пользователям "О сайте"
@login_required
def about(request):
    '''Пример использвоание класса Paginator в функции представления'''
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)  # По 3 элемента спсика на каждой странице

    page_number = request.GET.get('page')  # Принимает номер страницы
    page_obj = paginator.get_page(page_number)  # Формирует объект-список элементов текущей страницы
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


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


# def login(request):
#     return HttpResponse("Авторизация")


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
        # Для оптимизации SQL запросов используем .select_related('cat')
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        # Формируем контекст данных, которые уже сформированы базовым классом
        context = super().get_context_data(**kwargs)
        # # Берём первую запись из posts, и обращаемся к объекут, который берёт название, тут бдут выполняться 2 запроса
        # c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
        #                                     cat_selected=context['posts'][0].cat_id)

        # Оптимизированный SQL запрос
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                            cat_selected=c.pk)

        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    # form_class = UserCreationForm
    template_name = 'women/register.html'  # Ссылка на шаблон
    success_url = reverse_lazy('login')  # Перенапревление при регистрации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # Вызывается при успешной проверки формы регистрации, автоматически авторизируя пользователя после регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Авториизует пользователя
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    # Вместо этого метода можно использовать константу LOGIN_REDIRECT_URL в settings.py
    def get_success_url(self):
        return reverse_lazy('home')


# Функция представления. Вызывает функцию logut, чтобы пользователь мог выйти
def logout_user(request):
    logout(request)
    return redirect('login')
