# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from bank.models import State, City



class BloodSearchForm(forms.Form):

    state = forms.ModelChoiceField(queryset=State.objects.all(), required=True, label='State')
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=False, label='City')
    _BLOOD_GROUP_CHOICES = (
        ('', '---------'),  # Add an empty choice for no default selection
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    blood_group = forms.ChoiceField(choices=_BLOOD_GROUP_CHOICES, required=False, label='Blood Group')
    # blood_group = forms.MultipleChoiceField(choices=_BLOOD_GROUP_CHOICES, widget=forms.CheckboxSelectMultiple)


    def __init__(self, *args, **kwargs):
        super(BloodSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()  # Initially, no cities are selected

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                pass

        self.helper = FormHelper()
        self.helper.form_id = 'search-form'  # Set the form ID
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(Field('state', css_class='form-control', onchange="updateCities()"), css_class='col-md-6'),
            Div(Field('city', css_class='form-control'), css_class='col-md-6'),
            Div(Field('blood_group', css_class='form-control'), css_class='col-md-6'),
            Submit('submit', 'Search', css_class='btn btn-primary mt-2')
        )

