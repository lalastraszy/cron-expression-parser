import unittest

from cron_parser import Parser


class TestParse(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(1, 7)

    def test_joker(self):
        self.assertEqual(self.parser.run('*'), '1 2 3 4 5 6 7')

    def test_single_value(self):
        self.assertEqual(self.parser.run('5'), '5')

    def test_separate_values(self):
        self.assertEqual(self.parser.run('1,3,5'), '1 3 5')

    def test_range(self):
        self.assertEqual(self.parser.run('5-7'), '5 6 7')

    def test_step(self):
        self.assertEqual(self.parser.run('2/2'), '2 4 6')

    def test_step_with_joker(self):
        self.assertEqual(self.parser.run('*/7'), '1')

    def test_invalid_exr(self):
        with self.assertRaises(Exception):
            self.parser.run('1/*')

    def test_invalid_number_too_small(self):
        with self.assertRaises(Exception):
            self.parser.run('0')

    def test_invalid_number_too_high(self):
        with self.assertRaises(Exception):
            self.parser.run('8')
