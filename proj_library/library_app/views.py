from django.http import HttpResponse
from django.http import JsonResponse
from library_app.models import Loan, CustomUser
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
        labels.append(str(x['status']))
        data.append(x['count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })