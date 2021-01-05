import unittest
from ImportData import ImportData


class GetData(unittest.TestCase):
    def test_get_data_load_everything_correct(self):
        # Arrange
        import_data = ImportData.ImportData()

        # Act
        data = import_data.get_data("../../Data/test.csv")

        expected = [[1, 2], [3, 4], [5, 6], [7, 8]]
        result = data
        # Assert
        self.assertListEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
