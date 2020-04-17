class Macrolibrary:
    def __init__(self):
        self._library = [{}]
    
    def mbody(self, mname: str)->str:
        pass

    def increase_level(self)->None:
        self._library.append({})

    def decrease_level(self)->None:
        try :
            self._library.pop()
        except IndexError :
            pass

    def insert(self, macrodef: tuple)->None:
        pass

    @property
    def library(self):
        return self._library

    @library.setter
    def library(self, library):
        raise PermissionError("library cannot be assign")