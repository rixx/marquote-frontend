class BaseGenerator:

    @property
    @abstractmethod
    def sentence_model(self):
        pass

    def generate(self, *args, lookahead=3 **kwargs):
        project = self.sentence_model.objects.first().project
        sentence = [project.start_word]
        
        if not self.is_valid_lookahead(lookahead, project):
            # TODO: error handling
            return

    def is_valid_lookahead(self, lookahead, project):
        if not isinstance(lookahead, int):
            return False

        if not (1 < lookahead < project.max_lookahead):
            return False

        return True
