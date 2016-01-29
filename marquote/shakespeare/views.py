from django.shortcuts import render
from django.views.generic import View

from shakespeare.models import ShakespeareSentence


class IndexView(View):
    template_name = 'shakespeare/index.html'

    def get(self, request):
        context = {'project': ShakespeareSentence.get_or_create_project()}
        return render(request, self.template_name, {})
