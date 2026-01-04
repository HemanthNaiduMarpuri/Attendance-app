from django import forms
from .models import Period, TimeTable
from django.forms import ValidationError
from academics.models import Semester_Subject

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['semester', 'period_number', 'start_time', 'end_time']
        widgets = {
            'semester':forms.Select(attrs={'class':'form-control'}),
            'period_number':forms.NumberInput(attrs={'class':'form-control'}),
            'start_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
            'end_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'})
        }

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['section', 'day', 'period', 'subject', 'session_type', 'span_count']
        widgets = {
            'section':forms.Select(attrs={'class':'form-control'}),
            'day':forms.Select(attrs={'class':'form-control'}),
            'period':forms.Select(attrs={'class':'form-control'}),
            'subject':forms.Select(attrs={'class':'form-control'}),
            'session_type':forms.Select(attrs={'class':'form-control'}),
            'span_count':forms.NumberInput(attrs={'min':1, 'max':3,'class':'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()

        session_type = cleaned_data.get('session_type')
        span_count = cleaned_data.get('span_count')
        section = cleaned_data.get('section')
        period = cleaned_data.get('period')
        day = cleaned_data.get('day')
        subject = cleaned_data.get('subject')

        if not all([session_type, span_count, section, period, day]):
            return cleaned_data

        if session_type == 'Theory' and span_count != 1:
            raise ValidationError("Theory class must span 1 hrs")
        
        if session_type == 'Lab' and span_count != 3:
            raise ValidationError("Practical lab must span 3 hrs")
        
        new_start = period.period_number
        new_end = new_start + span_count - 1

        existing_entries = TimeTable.objects.filter(
            section = section,
            day = day
        ).order_by('period__period_number')

        if self.instance.pk:
            existing_entries = existing_entries.exclude(pk=self.instance.pk)

        for entry in existing_entries:
            existing_start = entry.period.period_number
            existing_end = existing_start + entry.span_count - 1

            overlap = not (new_end < existing_start or new_start > existing_end)

            if overlap:
                raise ValidationError(
                    f"Period conflict: overlaps with {entry.subject} "
                    f"(Periods {existing_start}–{existing_end})."
                )
        
        semester = section.semester

        if not Semester_Subject.objects.filter(
            semester=semester,
            subject=subject,
            status='Active'
        ).exists():
            raise ValidationError( "Selected subject is not mapped to this section's semester ""or is inactive.")

        return cleaned_data
    



    

            

