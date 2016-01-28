class BaseParser

    @property
    @abstractmethod
    def sentence_model(self):
        pass

    @abstractmethod
    def parse(self, *args, **kwargs):
        pass
