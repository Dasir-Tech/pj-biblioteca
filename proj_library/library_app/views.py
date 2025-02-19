from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Loan

def hello(request):
    return HttpResponse(" << Welcome into the Library_app >> ")

# Create your views here.


