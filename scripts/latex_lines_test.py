
import unittest
from latex_lines import LatexLine, latex_lines

class TestStringMethods(unittest.TestCase):

    def test_comment(self):
        lines = latex_lines("""This is normal text.
                            \jbgcomment{But this is a comment}
                            And this is not.
                            Then there's an inline one \foocomment{blarg}
                            """)

        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
