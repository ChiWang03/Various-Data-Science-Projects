import unittest
from anonymizer_test import TestAnonymizer
from evaluator_test import TestEvaluator

def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestAnonymizer))
    suite.addTest(unittest.makeSuite(TestEvaluator))
    runner = unittest.TextTestRunner()
    print (runner.run(suite))
    
my_suite()