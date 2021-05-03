from ImportData import ImportData
from Point import Point
from Paint import Painter
from Autoclust import Autoclust
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config_file = "config.ini"
    config.read(config_file)
    import_data = ImportData.ImportData()
    path_to_data = config['DEFAULT']['path_to_data']
    data_raw = import_data.get_data(path_to_data)
    points = []
    for row in data_raw:
        point = Point.Point()
        point.init_data(row)
        points.append(point)
    points.sort(key=lambda e: (e.y, e.x))

    painter = Painter.Painter()
    painter.set_to_paint = points
    painter.paint_points_by_label()

    # phase 1
    algorithm = Autoclust.Autoclust()
    algorithm.load_data(points)
    algorithm.make_triangulation()
    algorithm.print_ambiguities_from_triangulation()
    painter.paint_delaunay(algorithm.point_array, algorithm.tri)

    algorithm.get_edges()
    algorithm.calculate_local_mean()
    algorithm.calculate_local_st_dev()
    algorithm.calculate_mean_st_dev()
    algorithm.calculate_relative_st_dev()
    algorithm.sort_edges()
    other_edges = algorithm.get_other_edges()
    painter.paint_points_with_edges(algorithm.point_array, other_edges, "other_edges")

    # phase 2
    algorithm.create_clusters_by_other_edges()
    painter.paint_points_by_prediction("clusters")

    short_edges = algorithm.get_short_edges()
    painter.paint_points_with_edges(algorithm.point_array, short_edges, "short_edges")

    algorithm.check_assign_by_short_edges()
    painter.paint_points_by_prediction("phase2")

    # phase 3

    algorithm.calculate_second_order_local_mean()
    algorithm.erase_second_order_long_edges()
    short_edges = algorithm.get_short_edges()
    other_edges = algorithm.get_other_edges()
    painter.paint_points_with_edges(algorithm.point_array, short_edges + other_edges, "short_edges_other_edges")

    algorithm.create_clusters_by_other_edges()
    algorithm.check_assign_by_short_edges()
    painter.paint_points_by_prediction("phase3")
