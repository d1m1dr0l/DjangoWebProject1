"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm, BlogForm
from .forms import KotBlogForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.db import models
from .models import Blog
from .models import KotBlog
from .models import Comment      # использование модели комментариев
from .forms import CommentForm   # использование формы ввода комментария
from .forms import BlogForm



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Полезные ресурсы о кунах',
            'year':datetime.now().year,
        }
    )   
def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            form.save()
            data = dict()
            data['kot'] = form.cleaned_data['kot']
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['home'] = form.cleaned_data['home'] 
            data['message'] = form.cleaned_data['message']
            data['phone'] = form.cleaned_data['phone']
            data['email'] = form.cleaned_data['email']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data,
        }
     )
def registration(request):
    
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  # запрет админки
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False # не админ
            reg_f.date_joined = datetime.now() # дата регистрации 
            reg_f.last_login = datetime.now() # дата последней авторизации
            
            regform.save() # сохранение изменений после добавленных полей
            
            return redirect('home') # адрес на гл. страницу
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
        
            'regform': regform,
            
            'year':datetime.now().year,
        }
        )
def blog(request):
    """Редакция страницы блога."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()      # запрос на выбор всех статей блога из модели
    
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )
def blogpost(request, parametr):
    """Редакция страницы поста в блоге."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)                  # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    
    if request.method == "POST":                            # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user                 # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now()                 # добавляем в модель Комментария (Comment) текущую дат
            comment_f.post = Blog.objects.get(id=parametr)  # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save()                                # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    else:
        form = CommentForm()                                # создание формы для ввода комментария
       
    return render(
        request,
        'app/blogpost.html',
        {
        'title':post_1,
        'post_1': post_1,                               # передача конкретной статьи в шаблон веб-страницы
        'comments': comments,                           # передача всех комментариев к данной статье в шаблон веб-страницы
        'form': form,                                   # передача формы добавления комментария в шаблон веб-страницы
        'year': datetime.now().year,
        }
    )
def newpost(request):
    
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            return redirect('blog')
        
    else:
              blogform = BlogForm()
    return render(
            request,
            'app/newpost.html',
            {
                'title': 'Добавить статью блога',
                'blogform': blogform,
                'year': datetime.now().year,
            }
        )
def kotblog(request):
     
     kotiki = KotBlog.objects.all()

     assert isinstance(request, HttpRequest)
     return render(
          request,
          'app/kotblog.html',
          {
               'title': 'Наши воспитанники',
               'kotiki': kotiki,
               'year':datetime.now().year,
          }
     )
def vospitannik(request, parametr):
     
     assert isinstance(request, HttpRequest)
     kotik_1 = KotBlog.objects.get(id=parametr)
     return render(
          request,
          'app/vospitannik.html',
          {
               "kotik_1": kotik_1,
               'year':datetime.now().year,
          }
     )
def newvospitannik(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
        kotblogform = KotBlogForm(request.POST, request.FILES)
        if kotblogform.is_valid():
            kotblog_f = kotblogform.save(commit=False)
            kotblog_f.save()
            return redirect('kotblog')
        
    else:
        kotblogform = KotBlogForm()
    return render(
            request,
            'app/newvospitannik.html',
            {
                'kotblogform': kotblogform,
                'title': 'Добавить воспитанника',
                'year': datetime.now().year,
            }
    )