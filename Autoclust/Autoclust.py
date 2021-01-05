from scipy.spatial import Delaunay
import numpy as np
import math


def calculate_edge_length(edge):
    point_a = edge[0]
    point_b = edge[1]
    length = math.sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)
    return length


class Autoclust:
    def __init__(self):
        self.points = []
        self.tri = []
        self.point_array = np.empty([0, 0])
        self.mean_st_dev = 0
        self.other_edges = []
        self.short_edges = []
        self.new_class_number = 0
        self.clusters = []

    def load_data(self, data):
        points_coordinates = []
        for element in data:
            self.points.append(element)
            point = [element.x, element.y]
            points_coordinates.append(point)
        self.point_array = np.array(points_coordinates)

    def make_triangulation(self):
        self.tri = Delaunay(self.point_array)

    def get_edges(self):
        triangles = self.tri.simplices
        for triangle in triangles:
            edges = self.points[triangle[0]].edges
            edge = [self.points[triangle[0]], self.points[triangle[1]]]
            self.__add_unique_edge_to_edges(edge, edges)

            edges = self.points[triangle[1]].edges
            edge = [self.points[triangle[1]], self.points[triangle[2]]]
            self.__add_unique_edge_to_edges(edge, edges)

            edges = self.points[triangle[2]].edges
            edge = [self.points[triangle[2]], self.points[triangle[0]]]
            self.__add_unique_edge_to_edges(edge, edges)

            edges = self.points[triangle[1]].edges
            edge = [self.points[triangle[1]], self.points[triangle[0]]]
            self.__add_unique_edge_to_edges(edge, edges)

            edges = self.points[triangle[2]].edges
            edge = [self.points[triangle[2]], self.points[triangle[1]]]
            self.__add_unique_edge_to_edges(edge, edges)

            edges = self.points[triangle[0]].edges
            edge = [self.points[triangle[0]], self.points[triangle[2]]]
            self.__add_unique_edge_to_edges(edge, edges)

    @staticmethod
    def __add_unique_edge_to_edges(edge, edges):
        if edge not in edges:
            edges.append(edge)

    def calculate_local_mean(self):
        for point in self.points:
            number_of_edges = len(point.edges)
            for edge in point.edges:
                point.local_mean += calculate_edge_length(edge) / number_of_edges

    def calculate_local_st_dev(self):
        for point in self.points:
            number_of_edges = len(point.edges)
            sum_of_edge_squared_deviation = 0
            for edge in point.edges:
                sum_of_edge_squared_deviation += (point.local_mean - calculate_edge_length(edge))**2
            point.local_st_dev = math.sqrt(sum_of_edge_squared_deviation / number_of_edges)

    def calculate_mean_st_dev(self):
        number_of_points = len(self.points)
        for point in self.points:
            self.mean_st_dev += point.local_st_dev/number_of_points

    def calculate_relative_st_dev(self):
        for point in self.points:
            point.relative_st_dev = point.local_st_dev/self.mean_st_dev

    def sort_edges(self):
        for point in self.points:
            for edge in point.edges:
                edge_len = calculate_edge_length(edge)
                if edge_len < point.local_mean - self.mean_st_dev:
                    point.short_edges.append(edge)
                elif edge_len > point.local_mean + self.mean_st_dev:
                    point.long_edges.append(edge)
                else:
                    point.other_edges.append(edge)

    def get_other_edges(self):
        self.other_edges = []
        for point in self.points:
            for edge in point.other_edges:
                self.__add_unique_edge_to_edges(edge, self.other_edges)
        return self.other_edges

    def get_short_edges(self):
        self.short_edges = []
        for point in self.points:
            for edge in point.short_edges:
                self.__add_unique_edge_to_edges(edge, self.short_edges)
        return self.short_edges

    def create_clusters_by_other_edges(self):
        for point in self.points:
            if len(point.other_edges) >= 2:
                prediction = self.__find_prediction_in_other_edges(point.other_edges)
                self.__assign_class_to_point_in_edges(point, prediction, point.other_edges)
        self.__clean_clusters()

    def __find_prediction_in_other_edges(self, other_edges):
        for edge in other_edges:
            if edge[1].prediction != -1:
                return edge[1].prediction
        prediction = self.new_class_number
        self.__make_new_cluster()
        return prediction

    def __assign_class_to_point_in_edges(self, point, prediction, edges):
        for edge in edges:
            self.__assign_point_to_cluster(edge[1], prediction)

    def __make_new_cluster(self):
        self.clusters.append([])
        self.new_class_number += 1

    def __assign_point_to_cluster(self, point, cluster_number):
        if point.prediction != cluster_number:
            if point.prediction > -1:
                self.clusters[point.prediction].remove(point)
            point.prediction = cluster_number
            self.clusters[cluster_number].append(point)

    def __clean_clusters(self):
        clusters = [x for x in self.clusters if x != []]
        self.clusters = clusters
        self.clusters.sort(key=len, reverse=True)
        self.__redefine_classes()
        self.new_class_number = len(self.clusters) - 1

    def __redefine_classes(self):
        for i in range(len(self.clusters)):
            for point in self.clusters[i]:
                point.prediction = i

    def check_assign_by_short_edges(self):
        for point in self.points:
            connected_components = self.__get_non_trivial_connected_components_info(point.short_edges)
            connected_components.sort(key=lambda e: (e[1], -e[2]), reverse=True)
            if len(connected_components) > 0:
                prediction = connected_components[0][0]
                self.__assign_point_to_cluster(point, prediction)
                self.__remove_other_edges_connected_to_different_component(point)
                self.__remove_short_edges_connected_to_different_component(point)
        self.__clean_clusters()

    def __get_non_trivial_connected_components_info(self, edges):
        connected_components = []
        for edge in edges:
            prediction = edge[1].prediction
            if prediction != -1:
                if not self.__check_if_cluster_in_list(connected_components, prediction):
                    size_of_cluster = self.__get_size_of_cluster(prediction)
                    if size_of_cluster > 1:
                        edge_length = calculate_edge_length(edge)
                        cluster_info = [prediction, size_of_cluster, edge_length]
                        connected_components.append(cluster_info)
        return connected_components

    def __get_connected_components_info(self, edges):
        connected_components = []
        for edge in edges:
            prediction = edge[1].prediction
            if prediction != -1:
                if not self.__check_if_cluster_in_list(connected_components, prediction):
                    size_of_cluster = self.__get_size_of_cluster(prediction)
                    edge_length = calculate_edge_length(edge)
                    cluster_info = [prediction, size_of_cluster, edge_length]
                    connected_components.append(cluster_info)
        return connected_components

    @staticmethod
    def __check_if_cluster_in_list(connected_components, prediction):
        for component in connected_components:
            if component[0] == prediction:
                return True
        return False

    def __get_size_of_cluster(self, prediction):
        return len(self.clusters[prediction])

    @staticmethod
    def __remove_other_edges_connected_to_different_component(point):
        prediction = point.prediction
        for edge in point.other_edges:
            end_point_prediction = edge[1].prediction
            if end_point_prediction != prediction:
                point.other_edges = []

    @staticmethod
    def __remove_short_edges_connected_to_different_component(point):
        prediction = point.prediction
        for edge in point.short_edges:
            end_point_prediction = edge[1].prediction
            if end_point_prediction != prediction:
                point.short_edges.remove(edge)

    def erase_predictions(self):
        for point in self.points:
            point.prediction = -1
        self.clusters = []
        self.new_class_number = 0

    def print_ambiguities_from_triangulation(self):
        for tri in self.tri.simplices:
            p1 = self.point_array[tri[0]]
            p2 = self.point_array[tri[1]]
            p3 = self.point_array[tri[2]]
            cx, cy, r = self.define_circle(p1, p2, p3)
            for point in self.point_array:
                if not ((point == p1).all() or (point == p2).all() or (point == p3).all()):
                    if self.check_if_point_belong_to_circle(cx, cy, r, point):
                        print(point)


    @staticmethod
    def define_circle(p1, p2, p3):
        temp = p2[0] * p2[0] + p2[1] * p2[1]
        bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
        cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
        det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

        # Center of circle
        cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
        cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

        r = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
        return cx, cy, r

    @staticmethod
    def check_if_point_belong_to_circle(cx, cy, r, point):
        return ((point[0]-cx)**2 + (point[1]-cy)**2 - r**2) == 0

    def calculate_second_order_local_mean(self):
        size_of_second_order_neighborhood = 0
        for point in self.points:

            size_of_second_order_neighborhood += len(point.short_edges)
            for edge in point.short_edges:
                point.second_order_local_mean += calculate_edge_length(edge)

                size_of_second_order_neighborhood += len(edge[1].short_edges)
                for second_order_edge in edge[1].short_edges:
                    point.second_order_local_mean += calculate_edge_length(second_order_edge)

                size_of_second_order_neighborhood += len(edge[1].other_edges)
                for second_order_edge in edge[1].other_edges:
                    point.second_order_local_mean += calculate_edge_length(second_order_edge)

            size_of_second_order_neighborhood += len(point.other_edges)
            for edge in point.other_edges:
                point.second_order_local_mean += calculate_edge_length(edge)

                size_of_second_order_neighborhood += len(edge[1].short_edges)
                for second_order_edge in edge[1].short_edges:
                    point.second_order_local_mean += calculate_edge_length(second_order_edge)

                size_of_second_order_neighborhood += len(edge[1].other_edges)
                for second_order_edge in edge[1].other_edges:
                    point.second_order_local_mean += calculate_edge_length(second_order_edge)
            point.second_order_local_mean /= size_of_second_order_neighborhood

    def erase_second_order_long_edges(self):
        for point in self.points:
            for edge in point.short_edges:
                if calculate_edge_length(edge) > point.second_order_local_mean + self.mean_st_dev:
                    point.short_edges.remove(edge)
            for edge in point.other_edges:
                if calculate_edge_length(edge) > point.second_order_local_mean + self.mean_st_dev:
                    point.other_edges.remove(edge)

    def make_predictions(self):
        to_visit = self.points
        while to_visit:
            point = to_visit.pop()
            connected_components = self.__get_all_connected_components(point)
            if len(connected_components) > 0:
                prediction = connected_components[0][0]
            else:
                prediction = self.new_class_number
                self.__make_new_cluster()
            self.__assign_point_to_cluster(point, prediction)
            self.__assign_class_to_point_in_edges(point, prediction, point.short_edges + point.other_edges)
            self.__manage_connected_points(to_visit, point)
        self.__clean_clusters()

    def __get_all_connected_components(self, point):
        connected_components = self.__get_connected_components_info(point.short_edges + point.other_edges)
        connected_components.sort(key=lambda e: (e[1], -e[2]), reverse=True)
        return connected_components

    @staticmethod
    def __manage_connected_points(to_visit, point):
        for edge in point.other_edges + point.short_edges:
            if edge[1] in to_visit:
                to_visit.remove(edge[1])
                to_visit.append(edge[1])
