from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView


def store(request):
    context = {}
    return render(request, 'store.html', context)




