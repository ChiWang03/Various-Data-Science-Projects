from pseudonymizer import evaluator
import pandas as pd
import unittest

class TestEvaluator(unittest.TestCase):
    
    i=0
    def setUp(self):
        print ("Run the setUp for each testcase")
        TestEvaluator.i = TestEvaluator.i + 1
        
    def tearDown(self):
        print ("Completed running test_" + str(TestEvaluator.i) + " for the Evaluator class")
        
    @classmethod    
    def setUpClass(self):
        print ("Set up the once for running all the tests")
        self.ldiv = evaluator.Ldiversity('l_diversity', 'counter')
        
    @classmethod
    def tearDownClass(cls):
        print ("Completed running all testcases for the Evaluator class")
        
    def test_evaluator(self):
        
        # Run the testcase for the first test file
        df = pd.read_csv("creditcard.csv")    # sample testfile 
        quasis = ['DOB', 'postal_code', 'Sex']
        self.ldiv.setQuasiId(quasis)
        sensId = ['credit_security_code']
        self.ldiv.setSensitiveId(sensId)
        maxProb = self.ldiv.ldivMaxProb(df, quasis, sensId)
        
        # Retrieve the values set to the evaluator object to make sure they are set correctly 
        setquasis = self.ldiv.getQuasiId()
        setsensId =  self.ldiv.getSensitiveId()
        
        self.assertIn('DOB', setquasis)
        self.assertIn('postal_code', setquasis)
        self.assertIn('Sex', setquasis)
        self.assertIn('credit_security_code', setsensId)
        self.assertEqual(maxProb, 0.5)
        
    def test_evaluator2(self):
        
        # Run the testcase for the first test file
        df = pd.read_csv("testDataset.csv")    # sample testfile 
        quasis = ['DOB', 'postal_code']
        self.ldiv.setQuasiId(quasis)
        sensId = ['income']
        self.ldiv.setSensitiveId(sensId)
        maxProb = self.ldiv.ldivMaxProb(df, quasis, sensId)
        
        # Retrieve the values set to the evaluator object to make sure they are set correctly 
        setquasis = self.ldiv.getQuasiId()
        setsensId =  self.ldiv.getSensitiveId()
        
        self.assertIn('DOB', setquasis)
        self.assertIn('postal_code', setquasis)
        self.assertIn('income', setsensId)
        self.assertNotIn('companies',setquasis)
        self.assertEqual(maxProb, 0.3333333333333333)
    

unittest.main(argv=[''], verbosity=2, exit=False)