import unittest

from app import calculate_sample_size


class CalculatorTests(unittest.TestCase):
    def test_three_percent_case(self):
        result = calculate_sample_size(80, 20, 3)
        self.assertEqual(result["m"], 1328)
        self.assertAlmostEqual(result["low_rate"], 0.024)
        self.assertAlmostEqual(result["high_rate"], 0.036)

    def test_twelve_percent_case(self):
        result = calculate_sample_size(80, 20, 12)
        self.assertEqual(result["m"], 302)
        self.assertAlmostEqual(result["low_rate"], 0.096)
        self.assertAlmostEqual(result["high_rate"], 0.144)

    def test_invalid_values(self):
        for values in [(0, 20, 3), (80, 0, 3), (80, 20, 0), (100, 20, 3)]:
            with self.assertRaises(ValueError):
                calculate_sample_size(*values)


if __name__ == "__main__":
    unittest.main()
