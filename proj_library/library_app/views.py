from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    return HttpResponse(" << Welcome into the Library_app >> ")

# Create your views here.
# Crea la classe PRESTITI
