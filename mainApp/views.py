from django.shortcuts import render
from django.template import RequestContext
from .models import SiteSettings


def main_page_view(request):
    return render(request, "mainApp/main-page.html")

