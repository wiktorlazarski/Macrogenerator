import unittest
from .macrolibrary import Macrolibrary

class TestMacrolibrary(unittest.TestCase):
    '''
        Test cases of Macrolibrary class used in macrogenerator module.
    '''

    def __init__(self, *args, **kwargs):
        super(TestMacrolibrary, self).__init__(*args, **kwargs)
        self.macrolibrary = Macrolibrary()

    def test_init(self):
        init_size = 1
        self.assertEqual(init_size, len(self.macrolibrary.library))
        self.assertIsInstance(self.macrolibrary.library[0], dict)

    def test_increase_level(self):
        self.macrolibrary.increase_level()
        current_lvl = 1
        self.assertEqual(current_lvl, len(self.macrolibrary.library) - 1)
    
    def test_decrease_level(self):
        self.macrolibrary.decrease_level()
        current_lvl = 0
        try:
            self.macrolibrary.decrease_level()
            self.assertTrue(True)
        except IndexError:
            self.assertTrue(False, "Macrolibrary.decrease_level raised IndexError")

    def test_insert(self):
        self.macrolibrary.insert(("COMPILE", "g++"))
        zero_level_macrodef_cnt = 1
        self.assertEqual(len(self.macrolibrary.library[0]), zero_level_macrodef_cnt)
        
        with self.assertRaises(ValueError):
             self.macrolibrary.insert((1, 2, 3))
        with self.assertRaises(TypeError):
            self.macrolibrary.insert((1, 2))

    def test_mbody(self):
        self.macrolibrary.insert(("COMPILE", "g++"))
        mbody = self.macrolibrary.mbody("COMPILE")

        self.assertEqual(mbody, "g++")

        self.macrolibrary.increase_level()
        flevel_macrodef = ("NAME", "main.cpp")
        self.macrolibrary.insert(flevel_macrodef)
        self.assertEqual("main.cpp", self.macrolibrary.library[1]["NAME"])

        self.macrolibrary.decrease_level()
        with self.assertRaises(RuntimeError):
            self.macrolibrary.mbody("NAME")
