from django.db import models
from django.conf import settings
from Crypto.Cipher import AES


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


class BloodBank(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/img/bloodbank/")

    def __str__(self):
        return self.name


class Blood(models.Model):
    blood_group = models.CharField(
        max_length=100, choices=_BLOOD_GROUP_CHOICES)
    units = models.IntegerField(default=1)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)

    def __str__(self):
        return self.blood_group
