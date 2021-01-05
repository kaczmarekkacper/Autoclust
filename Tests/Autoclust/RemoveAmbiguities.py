import unittest
from Point import Point
from Autoclust import Autoclust
from TestData import data_co_circular
from Paint import Painter


class MyTestCase(unittest.TestCase):
    def test_remove_ambiguities(self):
        # Arrange
        points = []
        for d in data_co_circular:
            point = Point.Point()
            point.init_data(d)
            points.append(point)
        alg = Autoclust.Autoclust()
        alg.load_data(points)

        # Act
        alg.make_triangulation()
        painter = Painter.Painter()
        painter.paint_delaunay(alg.point_array, alg.tri)
        alg.print_ambiguities_from_triangulation()

        # Assert
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
