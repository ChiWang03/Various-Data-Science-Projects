import statswrangler.training as tr
import pandas as pd
import unittest
from pandas.util.testing import assert_frame_equal

#since training.py uses the .sample() function it is required to set seed or df.sample(random_state=1) to set seed as 1
#I have already modified the training.py module code so that it is df.sample(random_state=1)
#or else it will always be checking a random result, which would result in a Fail 

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
        
    
    def setUp(self):
        self.together = tr.TrainingData(df1).SplitTrain()
        self.train1, self.test1 = tr.TrainingData(df1).SplitTrain()
        self.train2, self.test2 = tr.TrainingData(df2).SplitTrain()
        self.train3, self.test3 = tr.TrainingData(df2,0.8).SplitTrain()
        print('Set Up')
        
    

    def test_SplitTrain(self): #test case
        #check if the function SplitTrain() returns a tuple 
        self.assertIs(type(self.together), type((2,2)) )
        
        #check if what is inside the tuple is a dataframe
        self.assertIs(type(self.train1), type(df1) )
        
        #test with pandas testing for dataframe
        #test each training and test set
        assert_frame_equal(self.train1, tr1)
        assert_frame_equal(self.test1, tt1) 
        
        assert_frame_equal(self.train2, tr2) 
        assert_frame_equal(self.test2, tt2) 
        
        assert_frame_equal(self.train3, tr3) 
        assert_frame_equal(self.test3, tt3) 
        
    def tearDown(self):
        print('Tear Down')
        
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')
unittest.main(argv=[''], verbosity=2, exit=False)   
