from django.db import models
from django.conf import settings
from Crypto.Cipher import AES

_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

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

_QUANTITY_CHOICES = (
    ('0.25' , '0.25'),
    ('0.5' , '0.5'),
    ('0.75' , '0.75'),
    ('1' , '1'),
)

_BED_TYPE_CHOICES = (
    ('General' , 'General'),
    ('ICU' , 'ICU'),
    ('Ventilator' , 'Ventilator'),
)

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    license = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/img/hospital/")

    def __str__(self):
        return self.name


class Bed(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE , null=True)
    type = models.CharField(max_length=100 , choices=_BED_TYPE_CHOICES, default='General')
    quantity = models.IntegerField(default=1)
    occupied = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.type + " " + str(self.quantity)


class BloodRequest(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE , null=True)
    blood_bank = models.ForeignKey("bank.BloodBank", on_delete=models.CASCADE,null=True)
    blood_group = models.CharField(max_length=100 , choices=_BLOOD_GROUP_CHOICES, default='A+')
    units = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status:str = models.CharField(max_length=100 , choices=_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.blood_group
    
    def decrypt(self):
        self.blood_group = str(self.blood_group).decode()
        self.status = self.status.decode()
        return self
    