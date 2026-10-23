import unittest
from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from grading_logic import determine_grade


class TestBatteryGrading(unittest.TestCase):

    def test_grade_a(self):
        self.assertEqual(determine_grade(95), "A")

    def test_grade_b(self):
        self.assertEqual(determine_grade(85), "B")

    def test_grade_c(self):
        self.assertEqual(determine_grade(70), "C")

    def test_grade_x(self):
        self.assertEqual(determine_grade(50), "X")


if __name__ == "__main__":
    unittest.main()
