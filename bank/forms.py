from django import forms

from crispy_forms.helper import FormHelper

from bank.models import BloodBank,Blood, State, City
from crispy_forms.layout import Layout, Div, Field, Submit


class BloodBankForm(forms.ModelForm):

    # hide password field
    password = forms.CharField(widget=forms.PasswordInput)
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=True, label='State')
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=True, label='City')

    class Meta:
        model = BloodBank
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BloodBankForm, self).__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/bank/add_bank/'
        # self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(Field('name', css_class='form-control'), css_class='mb-3'),
            Div(Field('phone', css_class='form-control'), css_class='mb-3'),
            Div(Field('email', css_class='form-control'),css_class='mb-3'),
            Div(Field('password', css_class='form-control'), css_class='mb-3'),
            Div(Field('state', css_class='form-control', onchange="updateCities()"), css_class='mb-3'),
            Div(Field('city', css_class='form-control'), css_class='mb-3'),
            Div(Field('license', css_class='form-control'), css_class='mb-3'),
            Div(Field('image', css_class='form-control'), css_class='mb-3'),
            Submit('submit', 'Submit', css_class='btn btn-primary mt-2')
        )

        # Set initial queryset for city field
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.all()


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