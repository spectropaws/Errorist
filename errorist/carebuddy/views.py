from django.shortcuts import render
from .constants import contacts

# Create your views here.


def home(request):
    return render(request, 'index.html', context=contacts.contact_details)


def patient(request):
    pass


def serviceproviders(request):
    pass