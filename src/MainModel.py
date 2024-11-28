from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

class MainModel(Model):
    #inheret methods from mesa Model class;J
    super.__init__; 

    def __init__(self, macrophage, fibroblast, cells):
       
        #Fields
        
        #lista för macrophages
        self.macList = [];
        self.fibList = [];
        self.cells = [];
        '''Other inhereted fields:
            running
            steps
            random
            rng
        '''

        #initiate game environment

        #initate objects

        #add objects to grid

        #initate grid

