import unittest
from Point import Point


class CheckPrediction(unittest.TestCase):
    def test_check_prediction_return_true_if_prediction_right(self):
        # Arrange
        point = Point.Point()
        point.label = 1
        point.prediction = 1

        # Act
        expected = True
        result = point.check_prediction()

        # Assert
        self.assertEqual(expected, result)

    def test_check_prediction_return_false_if_prediction_wrong(self):
        # Arrange
        point = Point.Point()
        point.label = 1
        point.prediction = 0

        # Act
        expected = False
        result = point.check_prediction()

        # Assert
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
