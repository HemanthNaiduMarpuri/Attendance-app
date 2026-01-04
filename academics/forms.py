from django import forms
from .models import Batch, Semester, Subject, Semester_Subject, Section

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['start_year', 'end_year']
        widgets = {
            'start_year' : forms.NumberInput(attrs={
                'min':1,
                'max':10000,
                'class':'form-control'
            }),
            'end_year' : forms.NumberInput(attrs={
                'min':1,
                'max':10000,
                'class':'form-control'
            })
        }
    def clean(self):
        if self.cleaned_data['start_year'] >= self.cleaned_data['end_year']:
            raise forms.ValidationError("End year should be grater than start year")
        
class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['batch', 'semester', 'semester_start_date', 'semester_end_date']
        widgets = {
            'batch':forms.Select(attrs={'class':'form-control'}),
            'semester':forms.Select(attrs={'class':'form-control'}),
            'semester_start_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'semester_end_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('semester_start_date')
        end = cleaned_data.get('semester_end_date')
        if start >= end:
            raise forms.ValidationError("Semester end date should be greater than start date")
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code', 'subject_name', 'subject_type']
        widgets = {
            'subject_code':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter the subject code'}),
            'subject_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter the subject name'}),
            'subject_type':forms.Select(attrs={'class':'form-control'})
        }

class SubjectMappingForm(forms.ModelForm):
    class Meta:
        model = Semester_Subject
        fields = ['semester', 'subject', 'status']
        widgets = {
            'semester':forms.Select(attrs={'class':'form-control'}),
            'subject':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'})
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['department_name', 'section', 'batch', 'semester']
        widgets = {
            'department_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter the department name'}),
            'section':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the section'}),
            'batch':forms.Select(attrs={'class':'form-control'}),
            'semester':forms.Select(attrs={'class':'form-control'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        batch = cleaned_data.get('batch')
        semester = cleaned_data.get('semester')
        if batch and semester:
            if semester.batch != batch:
                raise forms.ValidationError("Selected semester does not belong to the selected batch.")
        return cleaned_data     
