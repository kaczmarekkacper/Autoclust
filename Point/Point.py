class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.label = -1
        self.prediction = -1
        self.edges = []
        self.short_edges = []
        self.long_edges = []
        self.other_edges = []
        self.local_mean = 0
        self.local_st_dev = 0
        self.relative_st_dev = 0
        self.second_order_local_mean = 0

    def init_data(self, row):
        i = 0
        if len(row) == 3:
            self.label = row[i]
            i = i+1
        else:
            self.label = -1
        self.x = row[i]
        i = i + 1
        self.y = row[i]

    def check_prediction(self):
        return self.label == self.prediction

    def calculate_error(self):
        return self.label - self.prediction

    def get_edges_in_list(self):
        result = []
        for edge in self.edges:
            point_a = edge[0]
            point_b = edge[1]
            result.append([[point_a.x, point_a.y], [point_b.x, point_b.y]])
        return result
