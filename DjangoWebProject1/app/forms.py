"""
Definition of forms.
"""

import email
from email import message
from random import choices
from turtle import home
from django import forms
from django.forms.formsets import MIN_NUM_FORM_COUNT
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog
from .models import AnketaForm
from .models import KotBlog




class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
    
class AnketaForm(forms.ModelForm):
    class Meta:
        model = AnketaForm
        fields = "__all__" 

    
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment                     # используемая модель
        fields = ('text',)                  # требуется заполнить только поле text
        labels = {'text': "Комментарий"}    # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}
        
class KotBlogForm(forms.ModelForm):
    class Meta:
        model = KotBlog
        fields = ('klichka','kratko','opisanie','foto1','foto2','foto3','foto4',)
        labels = {'klichka':"Кличка",'kratko':"Немного о пушистом",'opisanie':"Полностью о пушистом",'foto1':"Фото 1",'foto2':"Фото 2",'foto3':"Фото 3",'foto4':"Фото 4"}
        
    
    
