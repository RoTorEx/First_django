from django.urls import path, re_path

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    # СВязали класс представления с маршруторм на главную страницу
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('addpage/', addpage, name='add_page'),
    # Прявяжем класс представления к маршруту
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    # Правило для маршрута
    # path('post/<slug:post_slug>/', show_post, name='post'),
    # Прявяжем класс представления к маршруту вместо предыдущего маршрута
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('category/<int:cat_id>/', show_category, name='category'),
    # Прявяжем класс представления к маршруту вместо предыдущего маршрута
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
