import unittest
from Point import Point


class InitData(unittest.TestCase):

    def test_init_data_assert_right_label(self):
        # Arrange
        row = [1, 2, 3]
        point = Point.Point()

        # Act
        point.init_data(row)

        expected = 1
        result = point.label
        # Assert
        self.assertEqual(expected, result)

    def test_init_data_assert_right_x(self):
        # Arrange
        row = [1, 2, 3]
        point = Point.Point()

        # Act
        point.init_data(row)

        expected = 2
        result = point.x
        # Assert
        self.assertEqual(expected, result)

    def test_init_data_assert_right_y(self):
        # Arrange
        row = [1, 2, 3]
        point = Point.Point()

        # Act
        point.init_data(row)

        expected = 3
        result = point.y
        # Assert
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
