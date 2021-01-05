import unittest
from Point import Point
from Autoclust import Autoclust
from TestData import data
import math

class CalculateLocalMean(unittest.TestCase):
    def test_calculate_local_mean(self):
        # Arrange
        points = []
        for d in data:
            point = Point.Point()
            point.init_data(d)
            points.append(point)
        alg = Autoclust.Autoclust()
        alg.load_data(points)

        # Act
        alg.make_triangulation()
        alg.get_edges()
        alg.calculate_local_mean()

        # Assert
        expected = (math.sqrt((1-0)**2 + (0-0)**2) + math.sqrt((1-0)**2+(1-0)**2) + math.sqrt((0-0)**2+(1.1-0)**2)) / 3
        actual = points[0].local_mean
        self.assertEqual(expected, actual)

        expected = (math.sqrt((0-0)**2 + (0-1.1)**2) + math.sqrt((1-0)**2+(1.1-1)**2)) / 2
        actual = points[1].local_mean
        self.assertEqual(expected, actual)

        expected = (math.sqrt((1-1)**2 + (1-0)**2) + math.sqrt((0-1)**2+(0-0)**2)) / 2
        actual = points[2].local_mean
        self.assertEqual(expected, actual)

        expected = (math.sqrt((0-1)**2 + (0-1)**2) + math.sqrt((1-1)**2+(0-1)**2) + math.sqrt((0-1)**2+(1.1-1)**2)) / 3
        actual = points[3].local_mean
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
