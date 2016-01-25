from django.db import models

from markov.models import BaseSentence, BaseProject


def get_shakespeare_project():
    project, created = BaseProject.objects.get_or_create(name='Shakespeare')

    if created:
        project.subtitle = 'Clever Shakespeare pun'
        project.max_lookahead = 5
        project.save()

    return project


class ShakespeareTitle(models.Model):
    SONNET = 'SO'
    PLAY = 'PL'
    FORM_CHOICES = (
        (SONNET, 'sonnet'),
        (PLAY, 'play'),
    )

    title = models.CharField(max_length=200)
    form = models.CharField(max_length=2, choices=FORM_CHOICES, default=PLAY)


class ShakespeareSentence(BaseSentence):
    title = models.ForeignKey(Title)

    def save(self, *args, **kwargs):
        if not self.project:
            self.project = get_shakespeare_project()
        super(ShakespeareSentence, self).save(*args, **kwargs)
