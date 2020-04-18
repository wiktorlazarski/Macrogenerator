class Macrolibrary:
    '''Class represents macrolibrary used in macrogenerator class.'''

    def __init__(self):
        self._library = [{}]
    
    def mbody(self, mname: str)->str:
        '''Returns macrodefinition body based on name priorities by text level.
            
            Parameters:
            mname (str): macrodefinition name which body we want to return.

            Returns:
            str: macrodefinition body
        '''
        for lvl_definitions in reversed(self.library):
            if mname in lvl_definitions:
                return lvl_definitions[mname]
        
        raise RuntimeError(f"unknown macrodefinition name: {mname}")

    def increase_level(self)->None:
        '''Increased text level by appending empty dict to the list representing library.'''
        self._library.append({})

    def decrease_level(self)->None:
        '''Decreased text level by popping dict from the list representing library.'''
        try :
            self._library.pop()
        except IndexError :
            return

    def insert(self, macrodef: tuple)->None:
        '''Inserts new macrodefinition at the currently specified text level.
            
            Parameters:
            macrodef (tuple): tuple containg two strings representing consecutively macroname and macrobody.
        '''
        MNAME_IDX = 0
        MBODY_IDX = 1

        if len(macrodef) != 2:
            raise ValueError("insert requires tuple of two strings")

        if not (isinstance(macrodef[MNAME_IDX], str) or isinstance(macrodef[MBODY_IDX], str)):
            raise TypeError("insert requires tuple of two strings")
        
        self.library[-1][macrodef[MNAME_IDX]] = macrodef[MBODY_IDX]


    @property
    def library(self):
        return self._library

    @library.setter
    def library(self, library):
        raise PermissionError("library cannot be assign")