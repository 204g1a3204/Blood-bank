from django.shortcuts import render, redirect
from django.http import JsonResponse
from e_blood_bank.forms import BloodSearchForm
from django.shortcuts import render, redirect
from donor.models import Donor
from bank.models import Blood, BloodBank
from hospital.models import Hospital
from django.db.models import Q
from itertools import groupby
from operator import itemgetter

from django.db.models import F, CharField, Value
from django.db.models.functions import Concat


def search_blood(req):
    print(req)
    if 'bank' in req.path:
        _SEARCH_BLOOD = 'bank/search-blood.html'
    elif 'hospital' in req.path:
        _SEARCH_BLOOD = 'hospital/search-blood.html'
    else:
        _SEARCH_BLOOD = 'donor/search-blood.html'

    if req.method == 'POST':
        form = BloodSearchForm(req.POST)
        if form.is_valid():
            state_id = req.POST.get('state')
            city_id = req.POST.get('city')
            blood_group = req.POST.get('blood_group')

            # Construct the base queryset based on state_id and city_id
            # queryset = Donor.objects.filter(Q(state_id=state_id) & Q(city_id=city_id))
            queryset = Donor.objects.filter(Q(state_id=state_id))

            # Optionally, filter by blood_group/city if it's provided
            if city_id:
                queryset = queryset.filter(city_id=city_id)
            if blood_group:
                queryset = queryset.filter(blood_group=blood_group)

            # queryset = Donor.objects.filter(Q(state_id=state_id) & Q(city_id=city_id) & Q(blood_group=blood_group))
            results = [{'name': donor.name, 'blood_group': donor.blood_group,
                        'phone': donor.phone, 'email': donor.email, 'type': 'donor',
                        'address': donor.address,
                        'date_of_birth': donor.date_of_birth} for donor in queryset]

            # queryset = Blood.objects.filter(Q(blood_bank__state_id=state_id) & Q(blood_bank__city_id=city_id))
            queryset = Blood.objects.filter(Q(blood_bank__state_id=state_id))

            # Optionally, filter by blood_group/city if it's provided
            if city_id:
                queryset = queryset.filter(blood_bank__city_id=city_id)

            if blood_group:
                queryset = queryset.filter(blood_group=blood_group)

            queryset = queryset.select_related('blood_bank', 'blood_bank__state', 'blood_bank__city')

            blood_banks = [{'name': b.blood_bank.name, 'blood_group': b.blood_group,
                            'phone': b.blood_bank.phone, 'email': b.blood_bank.email,
                            'type': 'Blood Bank', 'address': b.blood_bank.address,
                            'date_of_birth': ''} for b in queryset]
            print(blood_banks)
            results.extend(blood_banks)

            # queryset = Ho.objects.filter(Q(blood_bank__state_id=state_id))


            # Return JSON response
            return JsonResponse(results
                                , safe=False)
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
