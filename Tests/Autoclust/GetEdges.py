import unittest
from Point import Point
from Autoclust import Autoclust
from TestData import data


class GetEdges(unittest.TestCase):
    def test_get_edges_get_correct_edges(self):
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

        # Assert
        expected = [[[0, 0], [1, 0]], [[0, 0], [1, 1]], [[0, 0], [0, 1.1]]]
        actual = points[0].get_edges_in_list()
        self.assertListEqual(expected, actual)

        expected = [[[0, 1.1], [0, 0]], [[0, 1.1], [1, 1]]]
        actual = points[1].get_edges_in_list()
        self.assertListEqual(expected, actual)

        expected = [[[1, 0], [1, 1]], [[1, 0], [0, 0]]]
        actual = points[2].get_edges_in_list()
        self.assertListEqual(expected, actual)

        expected = [[[1, 1], [0, 0]], [[1, 1], [1, 0]], [[1, 1], [0, 1.1]]]
        actual = points[3].get_edges_in_list()
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
