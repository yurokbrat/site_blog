from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'admin_first_try_1',
        'title': 'Это первый пост',
        'content': 'Здесь находится содержание первого поста',
        'date_posted': '22.12.2023'
     },
    {
        'author': 'admin_second_try_1',
        'title': 'Это второй пост',
        'content': 'Здесь находится содержание второго поста',
        'date_posted': '22.12.2023'
    }
]


def home(request):
    return render(request, 'blog/home.html', context={'posts': posts})


def about(request):
    return render(request, 'blog/about.html', context={'title':'YuroKeep'})