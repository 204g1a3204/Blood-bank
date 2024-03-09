from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from donor.models import Donor
from bank.models import Blood, BloodBank
from donor.forms import DonorForm, BloodSearchForm
import os
import json
from bank.models import State, City

_INDEX_PAGE = 'index.html'
_LOGIN_PAGE = 'donor/login.html'
_HOME_PAGE = 'donor/home.html'
_ADD_DONOR = 'donor/add_donor.html'

_SEARCH_BLOOD = 'donor/search-blood.html'
_SEARCH_RESULTS = 'donor/search-results.html'



def index(req):
    return render(req, _INDEX_PAGE)


def logout(req):
    req.session.flush()
    return redirect('home')


def donor_login(req):
    if req.method == 'POST':
        try:
            email = req.POST.get('email')
            password = req.POST.get('password')
            donor = Donor.objects.get(email=email, password=password)
            print(donor.id)
            print(donor.name)
            req.session['donor'] = donor.id
            return redirect('donor_home')
        except Donor.DoesNotExist:
            return render(req, _LOGIN_PAGE, {'error': 'Invalid Credentials'})
    return render(req, _LOGIN_PAGE)


def home(req):
    donor = Donor.objects.filter(id=req.session['donor'])
    return render(req, _HOME_PAGE, {'donor': donor})


def add_donor(req):
    if req.method == 'POST':
        form = DonorForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect('donor_login')
        else:
            return render(req, _ADD_DONOR, {'form': form})
    else:
        form = DonorForm()
    return render(req, _ADD_DONOR, {'form': form})


