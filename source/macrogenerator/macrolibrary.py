class Macrolibrary:
    
    def __init__(self):
        self._library = [{}]
    
    def mbody(self, mname: str)->str:
        pass

    def increase_level(self)->None:
        pass

    def decrease_level(self)->None:
        pass

    @property
    def library(self):
        return self._library