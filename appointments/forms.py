from django import forms

from .models import TIME_CHOICES, Appointment, Doctor


class AppointmentForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    preferred_date = forms.DateField(
        label='Preferred Date',
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose Date',
            'id': 'dateSelect'
        })
    )
    available_time = forms.CharField(
        label='Available Time',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'timeSelect'
            },
            choices=TIME_CHOICES
        ),
    )
    doctor = forms.ModelChoiceField(
        label='Choose Doctor',
        empty_label='Choose Doctor',
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'doctorSelect'
        }),
    )
    message = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Message',
            'rows': '5'
        })
    )
