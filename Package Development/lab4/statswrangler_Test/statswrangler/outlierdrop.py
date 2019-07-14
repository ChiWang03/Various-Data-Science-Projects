import pandas as pd
import numpy as np

class Data: 
    def __init__(self, series, dataframe):
        self.series = series
        self.dataframe = dataframe
    #function that removes outliers in a dataframe based on the box plot 
    def Outliers(self):
        try: 
            #quartile 1 and quartile 2
            q1 = np.percentile(self.series, 25)
            q3 = np.percentile(self.series, 75)
            #interquartile change
            iqr = q3-q1
            #set lower upper bound
            lower = q1-(iqr*1.5)
            upper = q3+(iqr*1.5)
        
            index = []
            outliers = []
            for i in range(0,len(self.series)):
                if self.series[i] > upper or self.series[i] < lower:
                    index.append(i)
                    outliers.append(self.series[i])
            self.index = index
            self.outliers = outliers
            #return a tuple of the index of the outliers in the data 
            #and the outliers themselves
            return (self.index, self.outliers)
        except: 
            print("Can not find outliers")
            return False
    
class Dropped(Data):
    #threshold meaning the amount of outlier observations allowed to be dropped 
    def __init__(self,series, dataframe,threshold = 10):
        Data.__init__(self, series, dataframe)
        self.threshold = threshold

    def DropOutliers(self):
        try: 
            Data.Outliers(self)
        
            if len(self.index) <= self.threshold:
                self.index =self.index
            else:
                self.index = self.index[0:self.threshold]
            
            df = self.dataframe 
            l = self.index
            #now drop the entire row based on the location of outliers in the index
            return df.drop(df.index[l])
        except:
            print("Can not drop outliers")
            return False
