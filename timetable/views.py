from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Period, TimeTable
from .forms import PeriodForm, TimeTableForm
from django.views import generic
from academics.mixins import AdminRequiredMixin

class PeriodCreateView(AdminRequiredMixin, generic.CreateView):
    model = Period
    template_name = 'academics/period/periodcreate.html'
    form_class = PeriodForm

    def get_success_url(self):
        return reverse_lazy('period_list')

class PeriodUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Period
    template_name = 'academics/period/periodupdate.html'
    form_class = PeriodForm
    
    def get_success_url(self):
        return reverse_lazy('period_list')

class PeriodListView(AdminRequiredMixin, generic.ListView):
    model = Period
    template_name = 'academics/period/periodlist.html'
    context_object_name = 'periods'
    
class TimetableCreateView(AdminRequiredMixin, generic.CreateView):
    model = TimeTable
    form_class = TimeTableForm
    template_name = 'academics/timetable/timetablecreate.html'
    
    def get_success_url(self):
        return reverse_lazy('timetable_list')

class TimetableUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = TimeTable
    form_class = TimeTableForm
    template_name = 'academics/timetable/timetableupdate.html'
        
    def get_success_url(self):
        return reverse_lazy('timetable_list')


class TimetableListView(AdminRequiredMixin, generic.ListView):
    model = TimeTable
    template_name = 'academics/timetable/timetablelist.html'
    context_object_name = 'timetables'