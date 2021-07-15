import pandas as pd
import pickle
import json

class ClassificationModel:
    def __init__(self, name, model, features) -> None:
        """
            set the pickle model associated with this class
        Parameters
        ----------
            name: str
                Name of the model 
            model: str
                Model file path (pickle file) 
            features: list<str>
                List of features  
        """
        self.name = name
        self.model = model
        self.features = features
        self.savedModel = None
        self.extractModelFromModelFile()

    def extractModelFromModelFile(self):
        with open(self.model, 'rb') as file:
            self.savedModel = pickle.load(file)
   
    def getTestData(self, inputData):
        """
            Extract the input data (x) from the input data. Input data is a python list 
        
        Parameters
        ----------
            inputFile: str
                the Data input in json format 
        Returns
        ----------
            testData: list
                x_test
        """
        data = json.dumps(inputData)

        df = pd.read_json(data)
        x_test = df[self.features]
        return(x_test)
                   
    def predictNew(self, test_data_x):
        predictions = self.savedModel.predict(test_data_x)
        return(predictions)