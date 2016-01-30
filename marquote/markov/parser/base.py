class BaseParser

    @property
    @abstractmethod
    def sequence_model(self):
        pass

    @abstractmethod
    def parse(self, *args, **kwargs):
        pass
