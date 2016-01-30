import logging
import re

import requests

from markov.parser.base import BaseParser
from markov.models import (
    SequenceOrder,
    Word,
)
from shakespeare.models import (
    ShakespeareSequence,
    ShakespeareTitle,
)


class ShakespeareSonnetParser(BaseParser):
    sequence_model = ShakespeareSequence

    def __init__(self):
        self.title, created = ShakespeareTitle.objects.get_or_create(
            title='Shakespeare Sonnets',
            form=ShakespeareTitle.SONNET
        )

    def get_file(self, path):
        url = 'http://www.gutenberg.org/cache/epub/1041/pg1041.txt'
        response = requests.get(url)
        data = response.content

        with open(path, 'w') as f:
            f.write(data.decode('utf-8'))

    def format_file(self, path):
        start = 'by William Shakespeare'
        end = 'End of Project Gutenberg'
        part = -1

        with open(path, 'r') as dirty:
            with open('{}.clean'.format(path), 'w') as clean:
                for line in dirty:
                    if part == -1:
                        part = 0
                    elif part == 0 and start in line:
                        part = 1

                    elif part == 1 and end in line:
                        part = 2
                    else:
                        clean.write(line)

    def parse(self, path='shakespeare/sonnets.txt'):
        self.get_file(path)
        self.format_file(path)

        with open('{}.clean'.format(path), 'r') as sonnetfile:
            remainder = []
            project = self.sequence_model.get_or_create_project()

            for line in sonnetfile:
                line = line.strip()
                if line == '' or isroman(line):
                    # start new at a new sonnet (just in case a punctuation mark was missing)
                    remainder = []
                    continue

                sentences = re.split('\. |\? |! ', line)
                sentences = [sentence.split() for sentence in sentences]
                sentences[0] = remainder + sentences[0]

                if line.endswith(('.', '?', '!')):
                    remainder = sentences.pop(-1)

                for sentence in sentences:
                    words = [Word.objects.get_or_create(name=word)[0] for word in sentence]

                    for wordset in list_subsets(words, size=project.max_lookahead):
                        sequence = ShakespeareSequence(title=self.title, project=project)
                        sequence.save()

                        for i in range(len(wordset)):
                            SequenceOrder(word=wordset[i], sequence=sequence, position=i+1).save()


def isroman(literal):
    literal = literal.strip()
    roman_pattern = re.compile(""" # matches numbers up to 154 (largest sonnte)
        ^                   # beginning of string
        (C{0,1})            #
        (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                            #        or 50-80 (L, followed by 0 to 3 X's)
        (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                            #        or 5-8 (V, followed by 0 to 3 I's)
        $                   # end of string
    """)
    if roman_pattern.search(literal):
        logging.get_logger(__name__).warning('{} is a roman literal.'.format(literal))
    return roman_pattern.search(literal)


def list_subsets(l, size):
    if len(l) <= size:
        yield l
    else:
        for i in range(len(l) - size + 1):
            yield l[i:i+size]
