"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from library_app import views

app_name = "library_app"

admin.site.site_header = "Biblioteca_Dasir"
admin.site.site_title = "Dasir library."

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ajax-lost-books/", views.AjaxLostBooks, name='ajax-lost-books'),
    path("ajax-users-year/", views.UsersPerYear, name='ajax-users-year'),
    path("ajax-books-status/", views.BooksPerStatus, name='ajax-books-status'),
    path("ajax-users-book-genre/", views.UsersBookPerGenre, name="ajax-users-book-genre"),
    path("ajax-last-loans/", views.LastLoans, name="ajax-last-loans"),
    path("ajax-last-news/", views.LastNews, name="ajax-last-news"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
