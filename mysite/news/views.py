from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You successfully registered')
            return redirect('home')
        else:
            messages.error(request, 'Your registration failed')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', context={
        "form": form
    })


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', context={"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
            'aramhovhannisyan5555@gmail.com', ['aram_hovhannisyann_2022@mail.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'sent successfully')
                return redirect('contact')
            else:
                messages.error(request, 'sent error')
        else:
            messages.error(request, 'Validation error')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', context={
        "form": form
    })


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # mixin_prop = 'amnews'
    # extra_context = {'title': 'Home'}
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Home')
        # context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        # return News.objects.filter(Q(pk__in=[5, 6]) | Q(title__contains='2') & ~ Q(pk__lt='4'))
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id''
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    redirect_field_name = 'news/add_news.html'
    # success_url = reverse_lazy('home') to return in home page

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'AmNews'
#     }
#     return render(request, 'news/index.html', context)

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'category')

# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#
#     context = {
#         "news_item": news_item
#     }
#
#     return render(request, 'news/view_news.html' , context)


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             # news = News.objects.create(**form.cleaned_data) -- don't use
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', context={
#         "form": form
#     })
