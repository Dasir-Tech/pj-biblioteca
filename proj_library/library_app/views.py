from django.http import HttpResponse

def hello(request):
    return HttpResponse(" << Welcome into the Library_app >> ")
