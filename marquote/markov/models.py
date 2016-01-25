from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    subtitle = models.CharField(max_length=1000)
    icon = models.FilePathField()

    max_lookahead = models.PositiveIntegerField()


class BaseSentence(models.Model):
    project = models.ForeignKey('Project')
    words = models.ManyToManyField('Word', through='SentenceOrder')
    weight = models.IntegerField()

    class Meta:
        abstract = True

    def append_word(self):
        pass

    def get_words(self):
        for word in self.words.order_by('word_in_sentence'):
            yield word
    
    def __str__(self):
        return ' '.join(self.get_words())


class Sentence(BaseSentence):
    pass


class Word(models.Model):
    name = models.CharField(max_length=100, db_index=True, null=False, blank=False)

    def __str__(self):
        return self.name


class SentenceOrder(models.Model):
    word = models.ForeignKey('Word', related_name='word_in_sentence')
    sentence = models.ForeignKey('Sentence')
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ('position', )
