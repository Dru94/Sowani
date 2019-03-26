from django.forms import ModelForm
from .models import Location, Suburb, Category, Business, Menu, Reviews, Reservations, Promotion, Images
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from functools import partial
from django.forms import formset_factory
from django.forms import modelformset_factory, Textarea

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BusinessForm(ModelForm):
    class Meta:
        model = Business
        fields = [
            "location",
        	"suburb",
        	"category",
        	"name",
            "phone",
            "email",
        	"photos",
            "tags",
        	"description",
        	"openTime",
        	"closeTime",
        ]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = [
            "business",
            "comment",
            "rating",
            "user",
            "images",
        ]

        widgets = {
            'business': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'rating': forms.HiddenInput(),
            'comment': Textarea(attrs={'cols': 80, 'rows': 1}),
        }


class ReservationsForm(ModelForm):
    class Meta:
        model = Reservations
        fields = [
            "business",
            "user",
            "people",
            "amount",
            "date",
            "time",
        ]

        widgets = {
            'business': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'people': forms.TextInput(attrs={'placeholder': 'Number of people'}),
            'date': DateInput(attrs={'placeholder': 'Date'}),
        }



