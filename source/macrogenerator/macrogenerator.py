from .macrolibrary import Macrolibrary
import sys

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
                mname, offset = self.extract_mname(source_text[idx:])
                idx += offset
                mbody, offset = self.extract_mbody(source_text[idx:])
                idx += offset
                if source_text[idx].isspace():
                    idx += 1
                self.library.insert((mname, mbody))
            elif char == self.MACROCALL_DISCRIMINANT: #macrocall
                mname, offset = self.extract_mname(source_text[idx:])
                idx += offset
                output_text += self.macrocall(mname)
            else: #free text
                output_text += char

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
                break

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
                elif char == self.MACRODEF_DISCRIMINANT and text[offset].isalpha():
                    out_text += char
                    nested_macrodef, nested_off = self.extract_mbody(text[offset:])
                    out_text += nested_macrodef
                    out_text += self.MACRODEF_DISCRIMINANT
                    offset += nested_off
                else:
                    out_text += char
            except IndexError:
                raise RuntimeError("ERROR: extracting - end of source text")
            
        if not out_text:
            raise RuntimeError("ERROR: Macrobody unspecified")
        return (out_text, offset)

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