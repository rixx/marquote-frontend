from django.shortcuts import render
from django.views.generic import View

from shakespeare.models import ShakespeareSequence


class IndexView(View):
    template_name = 'shakespeare/index.html'

    def get(self, request):
        context = {'project': ShakespeareSequence.get_or_create_project()}
        return render(request, self.template_name, {})
