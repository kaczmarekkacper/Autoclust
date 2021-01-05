import csv
from operator import length_hint


class ImportData:
    def __init__(self):
        self.path = ""
        self.objects = [[]]

    def get_data(self, path):
        self.path = path
        with open(self.path, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        data = data[1:len(data)]
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                data[i][j] = float(data[i][j])
        self.objects = data
        return self.objects
