from django.shortcuts import render

from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import NewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 4  # количество записей на странице

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'flatpages/new.html'
    # Название объекта, в котором будет выбрана пользователем новость
    context_object_name = 'new'


class NewsSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search'
    paginate_by = 5  #  количество записей на странице

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = NewForm
    # модель новостей
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'flatpages/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/article/create':
            post.categoryType = 'AR'
        post.save()
        return super().form_valid(form)


class NewUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        #post.categoryType = 'NW'
        return super().form_valid(form)


# Представление удаляющее пост
class NewDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')
