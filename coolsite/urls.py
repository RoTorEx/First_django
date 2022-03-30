"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coolsite import settings
from women.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут-обращение к админке сайта
    path('women/', include('women.urls')),  # Предпочтительный вариант, вызывается функция include

    # '''Такое указание маршрутов, вручную, нарушает принцип независимости'''
    # path('women/', index),  # Определяем шаблон, и указываем ссылку на функцию, которая будет активизироваться запрос
    # path('', include('women.urls')),  # Маршрут к главной странице
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
