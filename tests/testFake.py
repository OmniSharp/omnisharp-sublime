import sublime, sys
from unittest import TestCase

version = sublime.version()

# module naming is different in ci than in sublime

omnisharp = sys.modules["OmniSharp"]


class test_fake(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fake_function(self):
        self.assertEqual(True, True)


class test_internal_functions(TestCase):
    def test_foo(self):
        self.assertEqual(True, True)
