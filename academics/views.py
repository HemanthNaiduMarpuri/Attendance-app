from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import BatchForm, SemesterForm, SubjectForm, SubjectMappingForm, SectionForm
from django.views import generic
from .models import Batch, Semester, Subject, Semester_Subject, Section
from django.db.models import Q
from .mixins import AdminRequiredMixin


class DashboardView(AdminRequiredMixin, generic.TemplateView):
    template_name = 'admin/dashboard.html'

class BatchCreateView(AdminRequiredMixin, generic.CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'academics/batch/batchform.html'

    def get_success_url(self):
        return reverse_lazy('batch_list')
    
class BatchListView(AdminRequiredMixin, generic.ListView):
    model = Batch
    template_name = 'academics/batch/batchlist.html'
    context_object_name = 'batches'

    def get_queryset(self):
        qs = Batch.objects.all()
        return qs

class BatchUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'academics/batch/batchform.html'

    def get_success_url(self):
        return reverse_lazy('batch_list')
        
class SemesterCreateView(AdminRequiredMixin, generic.CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'academics/semester/semestercreate.html'

    def get_success_url(self):
        return reverse_lazy('semester_list')

class SemesterListView(AdminRequiredMixin, generic.ListView):
    model = Semester
    template_name = 'academics/semester/semesterlist.html'
    context_object_name = 'semesters'

    def get_queryset(self):
        qs = super().get_queryset()
        batch = self.request.GET.get('batch')

        if batch:
            qs = qs.filter(batch__id = batch)
        return qs

class SubjectCreateView(AdminRequiredMixin, generic.CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject/subjectcreate.html'

    def get_success_url(self):
        return reverse_lazy('subject_list')
    
class SubjectUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject/subjectupdate.html'

    def get_success_url(self):
        return reverse_lazy('subject_list')
    
class SubjectListView(AdminRequiredMixin, generic.ListView):
    model = Subject
    template_name = 'academics/subject/subjectlist.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')

        if q:
            qs = qs.filter(Q(subject_name__icontains=q) | Q(subject_code__icontains=q))
        return qs

class SubjectMappingCreateView(AdminRequiredMixin, generic.CreateView):
    model = Semester_Subject
    form_class = SubjectMappingForm
    template_name = 'academics/subjectmapping/subjectmappingcreate.html'

    def get_success_url(self):
        return reverse_lazy('subject_semester_list')
    
class SubjectMappingUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Semester_Subject
    form_class = SubjectMappingForm
    template_name = 'academics/subjectmapping/subjectmappingupdate.html'

    def get_success_url(self):
        return reverse_lazy('subject_semester_list')
    
class SubjectMappingListView(AdminRequiredMixin, generic.ListView):
    model = Semester_Subject
    template_name = 'academics/subjectmapping/subjectmappinglist.html'
    context_object_name = 'mappings'

    def get_queryset(self):
        qs = super().get_queryset()
        semester_id = self.request.GET.get('semester')

        if semester_id:
            qs = qs.filter(semester__id = semester_id)
        return qs

class SectionCreationView(AdminRequiredMixin, generic.CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/section/sectioncreate.html'

    def get_success_url(self):
        return reverse_lazy('section_list')
    
class SectionUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/section/sectionupdate.html'
    

    def get_success_url(self):
        return reverse_lazy('section_list')    
    
class SectionListView(AdminRequiredMixin, generic.ListView):
    model = Section
    template_name = 'academics/section/sectionlist.html'
    context_object_name = 'sections'

    def get_queryset(self):
        qs = super().get_queryset()
        semester_id = self.request.GET.get('semester_id')
        if semester_id:
            qs = qs.filter(semester__id=semester_id)
        return qs
