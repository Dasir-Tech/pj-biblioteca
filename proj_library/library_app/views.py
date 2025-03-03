from django.http import HttpResponse
from django.http import JsonResponse
from library_app.models import Loan, CustomUser, Book
from django.db.models import Count

def hello(request):
    return HttpResponse(" << Welcome into the Library_app >> ")

def AjaxLostBooks(request):
    labels = []
    data = []

    queryset = Loan.objects.filter(status=3).values('due_date__year').annotate(count=Count("id")).order_by("due_date__year")
    for x in queryset:
        labels.append(str(x['due_date__year']))
        data.append(x['count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def UsersPerYear(request):
    labels = []
    data = []

    queryset = CustomUser.objects.values("date_joined__year").annotate(count=Count("id")).order_by("date_joined__year")
    for x in queryset:
        labels.append(str(x['date_joined__year']))
        data.append(x['count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def BooksPerStatus(request):
    labels = []
    data = []

    queryset = Loan.objects.values("status").annotate(count=Count("id")).order_by("status")
    for x in queryset:
        if x["status"] == 1:
            labels.append("Available")
            queryset = Book.objects.values("title").annotate(count=Count("id"))
            data.append(x["count"])
        elif x["status"] == 2:
            labels.append("On Loan")
        elif x["status"] == 3:
            labels.append("Lost")
        elif x["status"] == 4:
            labels.append("Damaged")

        data.append(x['count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def UsersBookPerGenre(request):
    labels = []
    data = []

    queryset = Loan.objects.values("book__genre__genre").annotate(count = Count("user", distinct=True)).order_by("book__genre__genre")
    for x in queryset:
        labels.append(str(x["book__genre__genre"]))
        data.append(x['count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })