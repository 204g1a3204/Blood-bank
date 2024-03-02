
from django.db import models
from django.conf import settings
from Crypto.Cipher import AES
from bank.models import State, City
import datetime

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


class Donor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=datetime.date(1900, 1, 1), null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    blood_group = models.CharField(
        max_length=100, choices=_BLOOD_GROUP_CHOICES)
    address = models.CharField(max_length=500, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name