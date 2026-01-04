from django.views import generic
from django.shortcuts import render

class HomePageView(generic.TemplateView):
    template_name = 'homepage.html'

def custom_403_view(request):
    return render(request, '403.html')