from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    # print(request)
    return HttpResponse('Hello world!')


def test(request, testid):
    return HttpResponse(f'this text %{testid}')
