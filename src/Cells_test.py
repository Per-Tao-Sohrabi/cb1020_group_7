from Cells import Cells
from MainModel import MainModel
import unittest

class CellTest(unittest.TestCase):

    def test_initiate(self):
        # Initialize MainModel object:
        model = MainModel()
        
        # Initialize a Cell object
        cell = Cells(1, model)

        # Test if model is an instance of MainModel
        self.assertIsInstance(model, MainModel)
        
        # Test if cell is an instance of Cells
        self.assertIsInstance(cell, Cells)

if __name__ == '__main__':
    unittest.main()
