from django import forms
from django.forms import ValidationError
from datetime import date as today_date


class AttendanceMarkForm(forms.Form):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent')
    )
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget= forms.RadioSelect
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data['date']

        if selected_date and selected_date > today_date.today():
            raise ValidationError("You can't mark Attendance for future dates.")
        
class HolidayMarkForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))

    def clean(self):
        selected_date = self.cleaned_data['date']

        if selected_date and selected_date > today_date.today():
            raise ValidationError("You can't mark holiday for future dates.")