from .macrolibrary import Macrolibrary

class Macrogenerator:
    _MACRODEF_DISCRIMINANT = '&'
    _MACROCALL_DISCRIMINANT = '$'
        
    def __init__(self):
        self.library = Macrolibrary()

    def transform(self, source_text: str)->str:
        pass

    def __macrodefinition(self)->None:
        pass

    def __macrocall(self, mname: str)->str:
        pass

    def __free_text(self)->str:
        pass

    @property
    def MACRODEF_DISCRIMINANT(self):
        return self._MACRODEF_DISCRIMINANT

    @MACRODEF_DISCRIMINANT.setter
    def MACRODEF_DISCRIMINANT(self, new):
        raise PermissionError("MACRODEF_DISCRIMINANT is a read only variable")
    
    @property
    def MACROCALL_DISCRIMINANT(self):
        return self._MACROCALL_DISCRIMINANT

    @MACROCALL_DISCRIMINANT.setter
    def MACROCALL_DISCRIMINANT(self, new):
        raise PermissionError("MACROCALL_DISCRIMINANT is a read only variable")