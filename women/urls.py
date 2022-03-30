from django.urls import path, re_path

from .views import *

urlpatterns = [
    # СВязали класс представления с маршруторм на главную страницу
    path('', WomenHome.as_view(), name='home'),
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
