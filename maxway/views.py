from django.shortcuts import render
from django.http import HttpResponse

def a(request):
    html = "<p>Salom</p>"
    return HttpResponse(html)

