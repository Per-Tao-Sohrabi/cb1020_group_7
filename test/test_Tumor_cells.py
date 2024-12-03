from src.Tumor_cells import Tumor_cells
from src.MainModel import MainModel
import unittest

class Test_Tumor_cells(unittest.TestCase):

    def test_initiate(self):
        # Initialize MainModel object:
        model = MainModel()
        
        # Initialize a Cell object
        tumor_cell = Tumor_cells(1, model)

        # Test if model is an instance of MainModel
        self.assertIsInstance(model, MainModel)
        
        # Test if cell is an instance of Cells
        self.assertIsInstance(tumor_cell, Tumor_cells)

if __name__ == '__main__':
    unittest.main()

