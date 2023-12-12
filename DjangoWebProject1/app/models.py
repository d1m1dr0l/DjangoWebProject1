"""
Definition of models.
"""

from tabnanny import verbose
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import CharField, ModelForm


class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    autor = models.ForeignKey(User,null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default= 'temp.jpg', verbose_name = 'Путь к картинке')    

    # Методы класса:
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    
    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title
    
    # Метаданные для доп. параметров модели:
    class Meta: 
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в админ. разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")
    
    # Методы класса:
    
    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)
    
    # Метаданные - вложенный класс, который задаёт дополнительные параметры модели:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
       
admin.site.register(Comment)

class AnketaForm(models.Model):
    kot = models.CharField(max_length=100, verbose_name='Кличка воспитанника', )
    name = models.CharField(max_length=100, verbose_name='Имя клиента', )
    city = models.CharField(max_length=100, verbose_name='В каком городе вы живёте?',)
    home = models.CharField(max_length=100, verbose_name='Квартира или загородный дом?',)
    message = models.TextField(verbose_name='Расскажите коротко о себе',)
    phone = models.CharField(max_length=100, verbose_name='Ваш номер телефона', )
    email = models.CharField(max_length=100,verbose_name='Ваша почта', )
    
    def get_absolute_url(self):
        return reverse('anketa', args=[str(self.id)])
    
    def __str__(self):
        return self.kot
    
    class Meta:
        db_table = "Ankety"
        verbose_name = "Анкета клиента"
        verbose_name_plural = "Анкеты клиентов"
        
admin.site.register(AnketaForm)

class KotBlog(models.Model):
    klichka = models.CharField(max_length = 100, verbose_name = "Кличка",)
    kratko = models.TextField(verbose_name = "Немного о пушистом",)
    opisanie = models.TextField(verbose_name = "Полное сожержание",)
    foto1 = models.FileField(default='temp.jpg', verbose_name="Путь к фото 1",)
    foto2 = models.FileField(default='temp.jpg', verbose_name="Путь к фото 2",)
    foto3 = models.FileField(default='temp.jpg', verbose_name="Путь к фото 3",)
    foto4 = models.FileField(default='temp.jpg', verbose_name="Путь к фото 4",)

    def ger_absolute_url(self):
        return reverse('vospitannik', args=[str(self.id)])
    def __str__(self):
        return self.klichka

    class Meta:
        db_table = "Kotiki"
        verbose_name = "Профиль воспитанника"
        verbose_name_plural = "Профили воспитанников"

admin.site.register(KotBlog)