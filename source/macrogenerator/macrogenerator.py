from .macrolibrary import Macrolibrary

class Macrogenerator:
    '''Class provides macrogenerator functionality.'''

    _MACRODEF_DISCRIMINANT = '&'
    _MACROCALL_DISCRIMINANT = '$'

    def __init__(self):
        self.library = Macrolibrary()

    def transform(self, source_text: str)->str:
        '''Transform input source text into output text.
            
            Parameters:
            source_text (str): source text containing macrodefinition/macrocalls/free texts.

            Returns:
            str: transformed text
        '''
        output_text = ""

        idx = 0
        while idx < len(source_text):
            char = source_text[idx]
            idx += 1

            if char == self.MACRODEF_DISCRIMINANT: #macrodefinition
                macrodef, offset = self._macrodefinition(source_text[idx:])
                self.library.insert(macrodef)
                idx += offset
            elif char == self.MACROCALL_DISCRIMINANT: #macrocall
                mname, offset = self._extract_mname(source_text[idx:])
                output_text += self._macrocall(mname)
                idx += offset
            else: #free text
                output_text += char

        return output_text

    def _macrodefinition(self, text: str)->tuple:
        '''Processes with macrodefinition when '&'-macrodefinition discriminant met.
            
            Parameters:
            text (str): not already processed source text.

            Returns:
            tuple: containg tuple=(mname, mbody) and offset, which represent number of character used while processing macrodefinition. 
        '''
        offset = 0
        mname, mname_offset = self._extract_mname(text)
        offset += mname_offset
        mbody, mbody_offset = self._extract_mbody(text[offset:])
        offset += mbody_offset
        # preserves macrocall discriminant or removes whitespace
        if text[offset].isspace():
            offset += 1
        
        return ((mname, mbody), offset)

    def _extract_mname(self, text: str)->tuple:
        '''Extract macrodefinition or macrocall name for further processing.
            
            Parameters:
            text (str): not already processed source text.

            Returns:
            tuple: containg macrodefinition name and offset, which represent number of character used while processing macrodefinition name. 
        '''
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

    def _extract_mbody(self, text: str)->tuple:
        '''Extract macrodefinition body for further processing.
            
            Parameters:
            text (str): not already processed source text.

            Returns:
            tuple: containg macrodefinition body and offset, which represent number of character used while processing macrodefinition body. 
        '''
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
                    nested_macrodef, nested_offset = self._extract_mbody(text[offset:])
                    retv += nested_macrodef
                    retv += self.MACRODEF_DISCRIMINANT
                    offset += nested_offset
                else:
                    retv += char
            except IndexError:
                raise RuntimeError("ERROR: extracting - end of source text")
            
        if not retv:
            raise RuntimeError("ERROR: macrobody unspecified")
        return (retv, offset)

    def _macrocall(self, mname: str)->str:
        '''Processes with macrocall when '$'-macrocall discriminant met.
            
            Parameters:
            mname (str): name of macrodefinition.

            Returns:
            str: free text resulted from macrocall. 
        '''
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