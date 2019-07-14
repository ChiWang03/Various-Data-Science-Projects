import unittest
import unittest1
import unittest2
def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(unittest1.TestOutlierdrop))
    suite.addTest(unittest.makeSuite(unittest2.TestTraining))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
my_suite()
