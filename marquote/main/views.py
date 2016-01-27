from django.shortcuts import render
from django.views.generic import View

from markov.models import Project


class IndexView(View):
    template_name = 'main/index.html'

    def get(self, request):
        context = {'all_projects': Project.objects.all(),
                   'base': 'base.html'}
        return render(request, self.template_name, context)
