class BaseGenerator:

    @property
    @abstractmethod
    def sequence_model(self):
        pass

    def get_project(self):
        return self.sequence_model.objects.first().project

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

    def pick_word(self, sequence, project):
        weights = dict()
        word_position = len(sequence) + 1
        all_sequences = project.sequence_set

        for db_sequence in all_sequences.objects.all():
            if _sequence_matches(db_sequence, sequence):
                word = db_sequence.words[word_position]
                # todo: defaultdict
                if word in weights.keys():
                    weights[word] += db_sequence.weight
                else:
                    weights[word] = db_sequence.weight

        return random.choice([word * weights[word] for word in weights.keys()])

    def format_sentence(self, sentence):
        return ' '.join(sentence) + '.'
