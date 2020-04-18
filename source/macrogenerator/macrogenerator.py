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
            idx += 1

            if char == self.MACRODEF_DISCRIMINANT: #macrodefinition
                macrodef, offset = self.macrodefinition(source_text[idx:])
                self.library.insert(macrodef)
                idx += offset
            elif char == self.MACROCALL_DISCRIMINANT: #macrocall
                mname, offset = self.extract_mname(source_text[idx:])
                output_text += self.macrocall(mname)
                idx += offset
            else: #free text
                output_text += char

        return output_text

    def macrodefinition(self, text: str)->tuple:
        offset = 0
        mname, mname_offset = self.extract_mname(text)
        offset += mname_offset
        mbody, mbody_offset = self.extract_mbody(text[offset:])
        offset += mbody_offset
        # preserves macrocall discriminant or removes whitespace
        if text[offset].isspace():
            offset += 1
        
        return ((mname, mbody), offset)

    def extract_mname(self, text: str)->tuple:
        retv = ""

        offset = 0
        while True:
            try:
                char = text[offset]
                offset += 1
                if char.isspace():
                    break
                retv += char
            except IndexError:
                break

        if not retv:
            raise RuntimeError("ERROR: macroname unspecified")
        return (retv, offset)

    def extract_mbody(self, text: str)->tuple:
        retv = ""

        offset = 0
        while True:
            try:
                char = text[offset]
                offset += 1
                if char == self.MACRODEF_DISCRIMINANT and (text[offset].isspace() or text[offset] == self.MACROCALL_DISCRIMINANT):
                    break
                elif char == self.MACRODEF_DISCRIMINANT and text[offset].isalpha():
                    retv += char
                    nested_macrodef, nested_offset = self.extract_mbody(text[offset:])
                    retv += nested_macrodef
                    retv += self.MACRODEF_DISCRIMINANT
                    offset += nested_offset
                else:
                    retv += char
            except IndexError:
                raise RuntimeError("ERROR: extracting - end of source text")
            
        if not retv:
            raise RuntimeError("ERROR: Macrobody unspecified")
        return (retv, offset)

    def macrocall(self, mname: str)->str:
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