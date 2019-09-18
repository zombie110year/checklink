import unittest as t


class TestCheckLink(t.TestCase):
    def test_version(self):
        from checklink import __version__
        self.assertEqual(__version__, "0.1.0")
