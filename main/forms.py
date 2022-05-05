from django import forms
from .models import Profile, Payment
from django.forms import ModelForm


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M', ])
    check_out = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M', ])

class HallAvailabilityForm(forms.Form):
    HALL_CATEGORIES = (
        ('KH', 'KINGDOM HALL'),
        ('MH', 'MISSION HALL'),
    )
    hall_category = forms.ChoiceField(choices=HALL_CATEGORIES, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M', ])
    check_out = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M', ])


class ProfileForm(forms.Form):
    title = forms.CharField()
    surName = forms.CharField()
    firstName = forms.CharField()
    address = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()
    telephone1 = forms.CharField()
    telephone2 = forms.CharField()
    contact_name = forms.CharField()
    contact_address = forms.CharField()
    contact_phone = forms.CharField()
    relationship = forms.CharField()
    idCard = forms.ImageField()

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = "__all__"

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount", "email")