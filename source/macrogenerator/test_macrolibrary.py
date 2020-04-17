import unittest
from .macrolibrary import Macrolibrary

class TestMacrolibrary(unittest.TestCase):
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
            self.assertTrue(False, "Macrolibrary.decrease_level raised IndexError")

    def test_insert(self):
        self.macrolibrary.insert(("COMPILE", "g++"))
        zero_level_macrodef_cnt = 1
        self.assertEqual(len(self.macrolibrary.library[0]), zero_level_macrodef_cnt)
        
        with self.assertRaises(ValueError):
             self.macrolibrary.insert((1, 2, 3))
        with self.assertRaises(TypeError):
            self.macrolibrary.insert((1, 2))