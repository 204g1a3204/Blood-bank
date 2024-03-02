from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms.widgets import Textarea

from .models import Hospital, Bed, BloodRequest


class HospitalForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_action = '/hospital/add_hospital/'

    # hide password field
    password = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField(widget=Textarea(attrs={'rows': 5}))

    class Meta:
        model = Hospital
        fields = "__all__"

class BedForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_action = '/hospital/add_bed/'
    helper.form_id = 'bed_form'

    class Meta:
        model = Bed
        fields = ('type', 'price', 'quantity','occupied')

class HospitalLoginForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.form_action = '/hospital/login/'

    class Meta:
        model = Hospital
        fields = ['email', 'password']


class BloodRequestForm(forms.ModelForm):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', 'Submit'))
        helper.form_action = '/hospital/raise_request/'
    
        class Meta:
            model = BloodRequest
            fields = ['blood_group', 'units' , 'blood_bank']


