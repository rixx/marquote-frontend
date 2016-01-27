from django.conf.urls import url

from main.views import IndexView


urlpatterns = [
    url(r'^$', IndexView.as_view()),
]
