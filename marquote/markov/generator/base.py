class BaseGenerator:

    @property
    @abstractmethod
    def sentence_model(self):
        pass

    def generate(self, *args, lookahead=3 **kwargs):
        project = self.sentence_model.objects.first().project
        sentence = [project.start_word]

        if lookahead < 1:
            return 

        if lookahead > project.max_lookahead:
            # raise OverflowError('Lookahead larger than allowed ({} > {}).'.format(lookahead, project.max_lookahead))
            # error handling
            return

