from django.db import models
from django.conf import settings
from Crypto.Cipher import AES
import os
import json

_BLOOD_GROUP_CHOICES = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# BASE_DIR = os.getcwd()
# states_path = os.path.join(BASE_DIR, 'e_blood_bank', 'states.json')
# cities_path = os.path.join(BASE_DIR, 'e_blood_bank', 'cities.json')
#
# # Read state data from state.json file
# with open(states_path, 'r') as state_file:
#     states = json.load(state_file)
#     state_choices = [(key, value) for key, value in states.items()]
#     print(state_choices)
# with open(cities_path, 'r') as state_file:
#     city_choices = json.load(state_file)
#     print(city_choices)

# state = forms.ModelChoiceField(queryset=State.objects.all(), required=True, label='State')
#     city = forms.ModelChoiceField(queryset=City.objects.none(), required=True, label='City')


class BloodBank(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    address = models.CharField(max_length=500, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="static/img/bloodbank/")

    def __str__(self):
        return self.name


class Blood(models.Model):
    blood_group = models.CharField(
        max_length=100, choices=_BLOOD_GROUP_CHOICES)
    units = models.IntegerField(default=1)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
