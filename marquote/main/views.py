from django.shortcuts import render

from markov.model import Project


class IndexView(View):
    template = 'main/index.html'

    def get(self, request):
        context = {'all_projects': Project.objects.all()}
        return render(request, self.template_name, context)
