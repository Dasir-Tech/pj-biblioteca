from django.http import HttpResponse
from django.http import JsonResponse
from library_app.models import Loan, CustomUser, Book, New
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BookForm, CustomUserForm
from .models import Book, CustomUser

def hello(request):
    return HttpResponse(" << Welcome into the Library_app >> ")

#Ajax Functions for Librarian Index

#Charts
#Data for Lost Books
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

#Data for Registered Users per Year
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

#Data for Status of the Books during time
def BooksPerStatus(request):
    labels = ["Never Loaned",]
    available = []
    onLoan = []
    lost = []
    damaged = []
    neverLoanedAvailable = []
    neverLoanedNotAvailable = []
    status = []
    y=0

    dateQuery = Loan.objects.values('update_date').distinct().order_by('update_date')
    for x in dateQuery:
        labels.append(str(x['update_date']))

    bookQuery = Book.objects.raw('select id, count(library_app_book.id) as count, library_app_book.qty\
        from library_app_book\
        where \
        not exists (\
            select 1\
            from \
            library_app_loan\
            where \
            book_ID = library_app_book.id\
        )\
        group by qty')
    sum = 0
    for x in bookQuery:
        if x.qty == 0:
            neverLoanedNotAvailable.append(x.count)
        else:
            sum = sum + x.count

    neverLoanedAvailable.append(sum)

    queryset = Loan.objects.raw("select id, count(distinct book_ID) as count, update_date, status\
        from library_app_loan\
        group by status, update_date\
        order by update_date;")
    for x in queryset:
        while y < len(labels):
            if str(x.update_date) == str(labels[y]):
                if x.status == 1:
                    status.append('Available')
                    available.append(x.count)
                elif x.status == 2:
                    status.append('On Loan')
                    onLoan.append(x.count)
                elif x.status == 3:
                    status.append('Lost')
                    lost.append(x.count)
                elif x.status == 4:
                    status.append('Damaged')
                    damaged.append(x.count)
            elif x.update_date and str(x.update_date) != str(labels[y]):
                try:
                    available[y]
                except:
                    available.append(0)
                try:
                    onLoan[y]
                except:
                    onLoan.append(0)
                try:
                    lost[y]
                except:
                    lost.append(0)
                try:
                    damaged[y]
                except:
                    damaged.append(0)
                y=y+1
                continue
            break
    try:
        available[y]
    except:
        available.append(0)
    try:
        onLoan[y]
    except:
        onLoan.append(0)
    try:
        lost[y]
    except:
        lost.append(0)
    try:
        damaged[y]
    except:
        damaged.append(0)


    return JsonResponse(data={
        'labels': labels,
        'available': available,
        'onLoan': onLoan,
        'lost': lost,
        'damaged': damaged,
        'neverLoanedAvailable': neverLoanedAvailable,
        'neverLoanedNotAvailable': neverLoanedNotAvailable,
        'status': status,
    })

#Data for Book Genre loaned by Users
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

#Tables
#Last 3 Loans
def LastLoans(request):
    queryset = Loan.objects.values('id', 'user__username', 'book__title', 'status', 'due_date', 'insert_date', 'update_date').filter(status = 2).order_by("update_date")[:3]

    data = {
        'loans': list(queryset)
    }

    return JsonResponse(data)

#Last 3 News
def LastNews(request):
    queryset = New.objects.values("id", "img", "header", "text", "insert_date", "update_date").order_by("-insert_date")[:3]

    data = {
        'news': list(queryset)
    }

    return JsonResponse(data)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = CustomUserForm()
    return render(request, 'add_user.html', {'form': form})