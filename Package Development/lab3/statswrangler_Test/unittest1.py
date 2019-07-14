import statswrangler.outlierdrop as od
import pandas as pd

import unittest
from pandas.util.testing import assert_frame_equal #this has to be imported to check dataframes

df = pd.read_csv("train.csv")

#data cleaning for test case checking later

df = df[0:100] #dataframe (will only use a subset dataset too big)

df = df.drop("PoolQC", axis = 1) #drop this columns since mostly NaN's

s1 = df["SalePrice"] #series 1 using column SalePrice
s2 = df["LotArea"] #series 2 using LotArea


#nooutliers1 and nooutliers2 will be used in our check cases

nooutliers1 = pd.read_csv("withnooutliers.csv", index_col = "Unnamed: 0")
#this dataset has already been cleaned so that outliers in SalePrice columnn have been removed
nooutliers1 = nooutliers1.drop("PoolQC", axis =1) #remove the PoolQC column since mostly NaN's


#nooutliers2 will refer to the testcase where threshold is 2
#this only removes 2 out of the 3 outliers in the dataset
#this dataset has the outliers in SalePrice columnn removed
nooutliers2 = pd.read_csv("withnooutliers2.csv",index_col = "Unnamed: 0")

class TestOutlierdrop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
    
    def setUp(self):
        self.d1 = od.Data(s1,df)
        self.d2 = od.Data(s2,df)
        self.d3 = od.Dropped(s1,df)
        self.d4 = od.Dropped(s2,df)
        self.d5 = od.Dropped(s1,df, threshold = 2) #with threshold = 2
        
        self.a1, self.b1 = self.d1.Outliers() 
        
        
        print('Set Up')
        
    def tearDown(self):
        print('Tear Down')
        
    def test_Outliers(self): #test case 
       
        self.assertIs(type(self.d1.Outliers()), type((2,3))) #check that it returns a tuple
        
        #check that they are lists, since the function that inherits this class will can only take lists 
        self.assertIs(type(self.a1) and type(self.b1), type([])) 
         
        
        #check for equal
        self.assertEqual(self.d1.Outliers(), ([11, 53, 58], [345000, 385000, 438780])) 
        self.assertEqual(self.d2.Outliers(), ([41, 53, 66, 75], [16905, 50271, 19900, 1596]))
        
        #check outliers in the series if they match the index
        for i in self.a1:
            self.assertIn(s1[i], self.b1)
            

        
    def test_DropOutliers(self): #test case
        #check the Outlier function could be used since there is inheritance
        self.assertEqual(self.d3.Outliers(), ([11, 53, 58], [345000, 385000, 438780]))
        self.assertEqual(self.d4.Outliers(), ([41, 53, 66, 75], [16905, 50271, 19900, 1596]))
        
        #check
        self.assertIs(type(self.d3.DropOutliers()), type(df)) #check that it returns a dataframe
        
        #I will only do two of the dataframe equilvalence checks since it's slightly complicated to clean data
        assert_frame_equal(self.d3.DropOutliers(), nooutliers1) #test with pandas testing for dataframe
        assert_frame_equal(self.d5.DropOutliers(), nooutliers2) #test with pandas testing for dataframe
        
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')
    
unittest.main(argv=[''], verbosity=2, exit=False)   
