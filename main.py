from ImportData import ImportData
from Point import Point
from Paint import Painter
from Autoclust import Autoclust

if __name__ == '__main__':
    import_data = ImportData.ImportData()
    template = "2d_dataset_{:d}.csv"
    template2 = "chameleon_ds{:d}.csv"
    which_data = 7
    data_raw = import_data.get_data("Data/" + template.format(which_data))
    points = []
    for row in data_raw:
        point = Point.Point()
        point.init_data(row)
        points.append(point)
    points.sort(key=lambda e: (e.y, e.x))

    painter = Painter.Painter()
    painter.set_to_paint = points
    painter.paint_points()

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
    painter.paint_points_with_edges(algorithm.point_array, other_edges)

    # phase 2
    algorithm.create_clusters_by_other_edges()
    painter.paint_points_by_prediction()

    short_edges = algorithm.get_short_edges()
    painter.paint_points_with_edges(algorithm.point_array, short_edges)

    algorithm.check_assign_by_short_edges()
    painter.paint_points_by_prediction()

    # phase 3

    algorithm.calculate_second_order_local_mean()
    algorithm.erase_second_order_long_edges()
    short_edges = algorithm.get_short_edges()
    other_edges = algorithm.get_other_edges()
    painter.paint_points_with_edges(algorithm.point_array, short_edges + other_edges)

    algorithm.erase_predictions()
    algorithm.make_predictions()
    painter.paint_points_by_prediction()
    painter.paint_points_by_label()
