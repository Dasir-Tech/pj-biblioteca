
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Loan
from django.http import JsonResponse
from library_app.models import Loan , CustomUser, Book, New 
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render




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

    queryset = Loan.objects.raw("select library_app_book.id, count(distinct library_app_book.id) as count, library_app_loan.update_date, library_app_loan.status from library_app_book left join library_app_loan on library_app_loan.book_ID = library_app_book.id group by library_app_loan.status, library_app_loan.update_date order by library_app_loan.update_date;")
    for x in queryset:
        if x.update_date:
            labels.append(x.update_date)
        else:
            labels.append('Never Loaned')
        data.append(x.count)

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
