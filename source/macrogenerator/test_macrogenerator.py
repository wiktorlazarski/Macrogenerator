import unittest
from .macrogenerator import Macrogenerator

class TestMacrogenerator(unittest.TestCase):

    # Correnct source text input cases
    def test_simple(self):
        macrogenerator = Macrogenerator()
        source_text = "&BASIC simple call& $BASIC";
        self.assertEqual(macrogenerator.transform(source_text), "simple call")

    def test_multiple_macrodef(self):
        macrogenerator = Macrogenerator()
        source_text = "&BASIC simple & &NAME call& $BASIC $NAME";
        self.assertEqual(macrogenerator.transform(source_text), "simple call")

    def test_nesting(self):
        macrogenerator = Macrogenerator()
        source_text = "&BASIC simple &NAME call&$NAME& $BASIC";
        self.assertEqual(macrogenerator.transform(source_text), "simple call")

    def test_proper_macrodef_for_text_level(self):
        macrogenerator = Macrogenerator()
        source_text = "&BASIC simple &BASIC call&$BASIC & $BASIC";
        self.assertEqual(macrogenerator.transform(source_text), "simple call")
    
    def test_close_discriminant_before_macrocall(self):
        macrogenerator = Macrogenerator()
        source_text = "&BASIC simple call&$BASIC";
        self.assertEqual(macrogenerator.transform(source_text), "simple call")