from django.db import models

from markov.models import Sequence, Project


class ShakespeareTitle(models.Model):
    SONNET = 'SO'
    PLAY = 'PL'
    FORM_CHOICES = (
        (SONNET, 'sonnet'),
        (PLAY, 'play'),
    )

    title = models.CharField(max_length=200, unique=True)
    form = models.CharField(max_length=2, choices=FORM_CHOICES, default=PLAY)


class ShakespeareSequence(Sequence):
    title = models.ForeignKey(ShakespeareTitle)

    def save(self, *args, **kwargs):
        if not self.project:
            self.project = self.get_or_create_project()
        super(ShakespeareSequence, self).save(*args, **kwargs)

    @staticmethod
    def _get_project_name():
        return 'Shakespeare'

    @classmethod
    def _create_project(cls):
        project = Project(name='Shakespeare',
                          subtitle='clever pun',
                          max_lookahead=5,
                          )
        project.save()
        return project
