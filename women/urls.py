from django.urls import path, re_path
from django.views.decorators.cache import cache_page  # Импортируем декоратор для кэширования

from .views import *

'''Функции представления оборачиваются в декоратор cache_page, а для классов его необходимо тут указать'''
urlpatterns = [
    # Связали класс представления с маршруторм на главную страницу
    path('', cache_page(60)(WomenHome.as_view()), name='home'),  # Время хранения кэша 1 минута. Кэщ главной страницы
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    # path('login/', login, name='login'),  # Простая заглушка авторизации
    # path('login/', LoginUser.as_view(), name='login'),  # Маршрут авторизации
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),  # Шаблон регистрации пользователей
    # path('post/<slug:post_slug>/', show_post, name='post'),
    # Прявяжем класс представления к маршруту вместо предыдущего маршрута
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<int:cat_id>/', show_category, name='category'),
    # Прявяжем класс представления к маршруту вместо предыдущего маршрута
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    # path('register/', login, name='register'),  # Простая заглушка регистрации
]
