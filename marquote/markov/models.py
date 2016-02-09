from django.db import models
from django.template.defaultfilters import slugify


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=40, unique=True)
    subtitle = models.CharField(max_length=1000)
    icon = models.FilePathField()
    start_word = models.CharField(max_length=30)
    end_word = models.CharField(max_length=30)

    max_lookahead = models.PositiveIntegerField()

    def save(self, **kwargs):
        if not self.pk:
            self.slug = self.slugify()
        super(Project, self).save()

    def slugify(self, slug_field='slug'):
        max_length = self.__class__._meta.get_field(slug_field).max_length
        long_slug = slugify(self.name)
        slug = slugify(self.name)[:max_length]
        tries = 0

        while self.__class__.objects.filter(slug=slug).exists():
            tries += 1
            ending = '-{}'.format(tries)
            slug = '{}{}'.format(long_slug[max_length-len(ending)], ending)

        return slug


class Sequence(models.Model):
    project = models.ForeignKey('Project')
    words = models.ManyToManyField('Word', through='SequenceOrder', null=True, blank=True)
    weight = models.IntegerField(default=1)

    def append_word(self):
        pass

    def get_words(self):
        for word in self.words.order_by('word_in_sequence'):
            yield word

    @classmethod
    def get_or_create_project(cls):
        project = Project.objects.filter(name=cls._get_project_name()).first()
        if not project:
            project = cls._create_project()

        return project

    def __str__(self):
        return ' '.join(self.get_words())


class Word(models.Model):
    name = models.CharField(max_length=100, db_index=True, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class SequenceOrder(models.Model):
    word = models.ForeignKey('Word', related_name='word_in_sequence')
    sequence = models.ForeignKey('Sequence')
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ('position', )
