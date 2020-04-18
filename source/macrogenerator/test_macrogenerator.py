import unittest
from .macrogenerator import Macrogenerator

class TestMacrogenerator(unittest.TestCase):
    '''
        Test cases class of Macrogenerator class used in macrogenerator module.
    '''

    def __init__(self, *args, **kwargs):
        super(TestMacrogenerator, self).__init__(*args, **kwargs)
        self.macrogenerator = Macrogenerator()

    # Correct source text input cases
    def test_simple(self):
        source_text = "&BASIC simple call& $BASIC";
        self.assertEqual(self.macrogenerator.transform(source_text), "simple call")

    def test_multiple_macrodef(self):
        source_text = "&BASIC simple & &NAME call& $BASIC $NAME";
        self.assertEqual(self.macrogenerator.transform(source_text), "simple call")

    def test_nesting(self):
        source_text = "&BASIC simple &NAME call&$NAME& $BASIC";
        self.assertEqual(self.macrogenerator.transform(source_text), "simple call")

    def test_proper_macrodef_for_text_level(self):
        source_text = "&BASIC simple &BASIC call&$BASIC & $BASIC";
        self.assertEqual(self.macrogenerator.transform(source_text), "simple call")
    
    def test_close_discriminant_before_macrocall(self):
        source_text = "&BASIC simple call&$BASIC";
        self.assertEqual(self.macrogenerator.transform(source_text), "simple call")

    # Incorrect source text input cases
    def test_unknown_macrodef(self):
        source_text = "&BASIC simple call& $BASE";
        with self.assertRaises(RuntimeError):
             self.macrogenerator.transform(source_text)
    
    def test_mname_unspecified(self):
        source_text = "& basic& $BASIC";
        with self.assertRaises(RuntimeError):
             self.macrogenerator.transform(source_text)

    def test_mbody_unspecified(self):
        source_text = "&BASIC & $BASE";
        with self.assertRaises(RuntimeError):
             self.macrogenerator.transform(source_text)

    def test_mdef_not_finished(self):
        source_text = "&BASIC simple call $BASE";
        with self.assertRaises(RuntimeError):
             self.macrogenerator.transform(source_text)
    
    def test_mdef_not_finished_nesting(self):
        source_text = "&BASIC simple &call $BASIC";
        with self.assertRaises(RuntimeError):
             self.macrogenerator.transform(source_text)