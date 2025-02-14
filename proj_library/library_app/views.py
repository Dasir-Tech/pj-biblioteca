from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse(" << Welcome into the Library >> ")

@home
def home(request):
    return render(request,'home.html') #-> template/home.html

@saluto
def saluto(request):
    return HttpResponse(f" << Welcome {nome}! >> ")

def contatto(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        return HttpResponse(f" << Welcome {nome}! >> ")
    return render(request,'contatto.html')
# Create your views here.
# Crea la classe PRESTITI
