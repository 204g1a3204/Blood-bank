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


def search_blood(req):
    if req.method == 'POST':
        form = BloodSearchForm(req.POST)
        if form.is_valid():
            state_id = req.POST.get('state')
            city_id = req.POST.get('city')
            blood_group = req.POST.get('blood_group')
            queryset = Donor.objects.filter(Q(state_id=state_id) & Q(city_id=city_id) & Q(blood_group=blood_group))
            donors = list(queryset.values())

            blood_banks_q = Blood.objects.filter(Q(blood_bank__state_id=state_id) & Q(blood_bank__city_id=city_id)).select_related('blood_bank')

            # model_b__some_field

            blood_banks = list(blood_banks_q.values())
            print(blood_banks)

            for blood_stock in blood_banks_q:
                print(blood_stock.blood_bank.name)  # Example access to BloodBank field
                print(blood_stock.blood_bank.phone)
                print(blood_stock.blood_bank.email)

            # queryset = Donor.objects.filter(Q(state_id=state_id) & Q(city_id=city_id) & Q(blood_group=blood_group))

            # queryset = BloodBank.objects.filter(Q(state_id=state_id) & Q(city_id=city_id))
            # donors = list(queryset.values())
            # print(donors)

            # Return JSON response
            return JsonResponse(donors, safe=False)
            # Process the form data here
            # state = form.cleaned_data['state']
            # city = form.cleaned_data['city']
            # Perform search operation using state and city
            # return redirect('bank_login')
        else:
            return render(req, _SEARCH_BLOOD, {'form': form})
    else:
        form = BloodSearchForm()
    return render(req, _SEARCH_BLOOD, {'form': form})
