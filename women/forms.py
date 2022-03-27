from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.ModelForm):  # При создании экземпляра формы 
    def __init__(self, *args, **kwargs):  # Инициализирует конструктор
        super().__init__(*args, **kwargs)  # Инициализирует конструктор базового класса
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women  # Связь формы с моделью Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']  # Список полей c model
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),  # Определяем стиль для поля title
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),  # Определяем стиль для поля content
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title
