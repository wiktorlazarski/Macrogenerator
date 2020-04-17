from .macrolibrary import Macrolibrary

class Macrogenerator:
    _MACRODEF_DISCRIMINANT = '&'
    _MACROCALL_DISCRIMINANT = '$'
        
    def __init__(self):
        self.library = Macrolibrary()

    def transform(self, source_text: str)->str:
        output_text = ""
       
        idx = 0
        while idx < len(source_text):
            char = source_text[idx]

            if char == self.MACRODEF_DISCRIMINANT: #macrodefinition
                idx += 1
                mname, offset = self.extract_mname(source_text[idx:])
                idx += offset
                mbody, offset = self.extract_mbody(source_text[idx:])
                idx += offset + 1
                self.library.insert((mname, mbody))
            elif char == self.MACROCALL_DISCRIMINANT: #macrocall
                mname, offset = self.extract_mname(source_text[idx + 1:])
                idx += offset + 1
                output_text += self.__macrocall(mname)
            else: #free text
                output_text += char
                idx += 1

        return output_text

    def extract_mname(self, text: str)->tuple:
        offset = 0
        out_text = ""

        while True:
            try:
                char = text[offset]
                offset += 1
                if char.isspace():
                    break
                out_text += char
            except IndexError:
                return (out_text, offset)

        if not out_text:
            raise RuntimeError("ERROR: Macroname unspecified")
        return (out_text, offset)

    def extract_mbody(self, text: str)->tuple:
        offset = 0
        out_text = ""

        while True:
            try:
                char = text[offset]
                offset += 1
                if char == self.MACRODEF_DISCRIMINANT and (text[offset].isspace() or text[offset] == self.MACROCALL_DISCRIMINANT):
                    break
                out_text += char
            except IndexError:
                raise RuntimeError("ERROR: extracting - end of source text")
        
        if not out_text:
            raise RuntimeError("ERROR: Macrobody unspecified")
        return (out_text, offset)

    def __macrocall(self, mname: str)->str:
        self.library.increase_level()
        mbody = self.library.mbody(mname)
        retv = self.transform(mbody)
        self.library.decrease_level()
        return retv

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