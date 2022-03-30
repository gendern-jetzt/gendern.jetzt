import unittest

from auto_deg_re import auto_deg_re

SYMS = [":", "*", "/", "_"]


class TestAutoDegRe(unittest.TestCase):
    def test_pronounce(self):
        for sym in SYMS:
            self.assertEqual(auto_deg_re("er" + sym + "sie"), "er")
            self.assertEqual(auto_deg_re("Sie" + sym + "Er"), "Er")
            self.assertEqual(auto_deg_re("ihr" + sym + "ihm"), "ihm")
            self.assertEqual(auto_deg_re("Ihm" + sym + "ihr"), "Ihm")
            self.assertEqual(auto_deg_re("sie" + sym + "ihn"), "ihn")


if __name__ == "__main__":
    unittest.main()
