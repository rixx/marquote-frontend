class BaseGenerator:

    @property
    @abstractmethod
    def sentence_model(self):
        pass

    def get_project(self):
        return self.sentence_model.objects.first().project

    def generate(self, *args, lookahead=3 **kwargs):
        project = self.get_project()
        sentence = [self.project.start_word]
        
        if not self.is_valid_lookahead(lookahead, project):
            # TODO: error handling
            return

        # TODO: loop detection
        while sentence[-1] != project.end_word:
            sequence = sentence[-lookahead:]
            sentence.append(self.pick_word(sequence, project))

        return self.format_sentence(sentence)

    def is_valid_lookahead(self, lookahead, project):
        if not isinstance(lookahead, int):
            return False

        if not (1 < lookahead < project.max_lookahead):
            return False

        return True

    def pick_next_sentence(self, sequence, project):
        weights = dict()
        word_position = len(sequence) + 1
        all_sentences = project.sentence_set

        for sentence in all_sentences.objects.all():
            if sentence_matches_sequence(sentence, sequence):
                word = sentence.words[word_position]
                # todo: defaultdict
                if word in weights.keys():
                    weights[word] += sentence.weight
                else:
                    weights[word] = sentence.weight

        return random.choice([word * weights[word] for word in weights.keys()])

    def format_sentence(self, sentence):
        return ' '.join(sentence) + '.'
