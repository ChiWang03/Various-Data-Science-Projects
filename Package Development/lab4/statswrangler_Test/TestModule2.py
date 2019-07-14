
# coding: utf-8

# In[108]:


import test2.training as tr
import pandas as pd
import unittest
from pandas.util.testing import assert_frame_equal


#since it uses the .sample() function it is required to set seed or df.sample(random_state=1) to set seed as 1 
#we will have to alter the module or else the test would fail 


# In[109]:


df0 = pd.read_csv("train.csv")
df1 = df0[0:30] #dataframe (will only use a subset dataset too big)


#some data cleaning before using the dataset
df1 = df1.drop("PoolQC", axis = 1) #since mostly NaN
df1 = df1.drop("Alley", axis = 1) #since mostly NaN
df1 = df1.drop("MiscFeature", axis = 1) #since mostly NaN

df2 = df0[30:60]
df2 = df2.drop("PoolQC", axis = 1) 
df2 = df2.drop("Alley", axis = 1)
df2 = df2.drop("MiscFeature", axis = 1)

#testing data for the test class
tr1 = pd.read_csv("train1.csv", index_col="Unnamed: 0")
tt1 = pd.read_csv("test1.csv", index_col="Unnamed: 0")

tr2 = pd.read_csv("train2.csv", index_col="Unnamed: 0")
tt2 = pd.read_csv("test2.csv", index_col="Unnamed: 0")

tr3 = pd.read_csv("train3.csv", index_col="Unnamed: 0")
tt3 = pd.read_csv("test3.csv", index_col="Unnamed: 0")


# In[110]:


class TestTraining(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')
    def setUp(self):
        self.train1, self.test1 = tr.TrainingData(df1).SplitTrain()
        self.train2, self.test2 = tr.TrainingData(df2).SplitTrain()
        self.train3, self.test3 = tr.TrainingData(df2,0.8).SplitTrain()
        print('Set Up')
        
    def tearDown(self):
        print('Tear Down')

    def test_SplitTrain(self): #test case
        assert_frame_equal(self.train1, tr1) #test with pandas testing for dataframe
        assert_frame_equal(self.test1, tt1) 
        
        assert_frame_equal(self.train2, tr2) 
        assert_frame_equal(self.test2, tt2) 
        
        assert_frame_equal(self.train3, tr3) 
        assert_frame_equal(self.test3, tt3) 
        
unittest.main(argv=[''], verbosity=2, exit=False)   


# In[ ]:




