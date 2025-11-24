import unittest

class SmokeTest(unittest.TestCase):
    def test_smoke(self):
        # A trivial test so unittest discover picks up something
        self.assertEqual(1 + 1, 2)

if __name__ == "__main__":
    unittest.main()
