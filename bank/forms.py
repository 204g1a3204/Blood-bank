from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import BloodBank,Blood


class BloodBankForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BloodBankForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/bank/add_bank/'
        self.helper.add_input(Submit('submit', 'Submit'))


class BloodForm(forms.ModelForm):
    class Meta:
        model = Blood
        fields = ('blood_group', 'units')

    def __init__(self, *args, **kwargs):
        super(BloodForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/bank/add_blood/'
        self.helper.form_id = 'blood_form'
        self.helper.add_input(Submit('submit', 'Submit'))