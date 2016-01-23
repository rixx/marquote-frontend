from django.db import models


class Word(models.Model):
    name = models.CharField(max_length=100, db_index=True, null=False, blank=False)

    def __str__(self):
        return self.name


class BaseSentence(models.Model):
    project = models.ForeignKey(Project)
    words = models.ManyToManyField(Word, through=SentenceOrder)

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


class SentenceOrder(models.Model):
    word = models.ForeignKey(Word, related_name='word_in_sentence')
    sentence = models.ForeignKey(Sentence)
    position = models.PositiveIntegerField(max_value=10)

    class Meta:
        ordering = ('position', )


class BaseProject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    subtitle = models.CharField(max_length=1000)
    icon = models.ImageField()

    max_lookahead = models.PositiveIntegerField(max_value=10)
    parser = models.CharField(max_length=100)
