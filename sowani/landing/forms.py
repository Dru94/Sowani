from django import forms
from .models import Email

class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ('email',)
        widgets={
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email'})
        }