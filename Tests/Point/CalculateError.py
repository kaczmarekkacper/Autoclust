import unittest
from Point import Point


class CalculateError(unittest.TestCase):
    def test_calculate_error_return_zero_if_prediction_right(self):
        # Arrange
        point = Point.Point()
        point.label = 1
        point.prediction = 1

        # Act
        expected = 0
        result = point.calculate_error()

        # Assert
        self.assertEqual(expected, result)

    def test_calculate_error_return_one_if_prediction_wrong(self):
        # Arrange
        point = Point.Point()
        point.label = 1
        point.prediction = 0

        # Act
        expected = 1
        result = point.calculate_error()

        # Assert
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
