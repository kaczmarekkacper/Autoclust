import matplotlib.pyplot as plt
from Colors import Colors


class Painter:
    def __init__(self):
        self.set_to_paint = []
        self.formatted_set = {}

    def paint_points(self):
        self.__format_set()
        plt.scatter(self.formatted_set["x"], self.formatted_set["y"], c=Colors.Colors["DARK_GREEN"])
        plt.show()

    def __format_set(self):
        self.formatted_set = {"x": [], "y": [], "label": [], "prediction": []}
        for point in self.set_to_paint:
            self.formatted_set['x'].append(point.x)
            self.formatted_set['y'].append(point.y)
            self.formatted_set['label'].append(point.label)
            self.formatted_set['prediction'].append(point.prediction)

    def paint_points_by_label(self):
        self.__format_set()
        plt.scatter(self.formatted_set["x"], self.formatted_set["y"],
                    c=self.formatted_set["label"])
        plt.savefig('ByLabel.png')
        plt.show()


    def paint_points_by_prediction(self, title):
        self.__format_set()
        plt.scatter(self.formatted_set["x"], self.formatted_set["y"],
                    c=self.formatted_set["prediction"])
        plt.savefig(f'{title}.png')
        plt.show()

    @staticmethod
    def paint_delaunay(points, tri):
        plt.triplot(points[:, 0], points[:, 1], tri.simplices)
        plt.scatter(points[:, 0], points[:, 1], c=Colors.Colors["DARK_GREEN"])
        plt.savefig('Delaunay.png')
        plt.show()

    @staticmethod
    def paint_points_with_edges(points, edges, title):
        for edge in edges:
            plt.plot([edge[0].x, edge[1].x], [edge[0].y, edge[1].y], c=Colors.Colors["BLUE"])
        plt.scatter(points[:, 0], points[:, 1], c=Colors.Colors["DARK_GREEN"])
        plt.savefig(f'{title}.png')
        plt.show()
