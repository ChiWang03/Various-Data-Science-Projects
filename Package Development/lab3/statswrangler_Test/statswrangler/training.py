
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np



class TrainingData:
    #percentage = percetage to be trained use decimal [0 to 1]
    #We set default to 0.5 since 50% training and 50% 
    #This isn't necessarily the best case since it really depends on the dataset
    def __init__(self, dataframe, percentage = 0.5):
        self.dataframe = dataframe
        self.percentage = percentage
    def SplitTrain(self):
        rows = len(self.dataframe)
        train = round(rows*self.percentage) # the number of rows used in the training data
        #test = rows-train # the number of rows used in the test data
        data = self.dataframe
 
        #drop = True, will keep its index without replacing it with a new index
        df = data.sample(frac=1, random_state=1).reset_index(drop=True)
        trainingdata = df[0:train]
        testdata = df[train:rows]
        
        
        return (trainingdata, testdata)
    
    

