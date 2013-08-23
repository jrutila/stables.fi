import os
from django.shortcuts import render


def home(request):
    tenant = request.tenant
    return render(request, 'home/home.html', { 'tenant': tenant })
