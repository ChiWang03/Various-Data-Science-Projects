
# Documentation 

## statswrangler package

### outlierdrop module
* The OutlierDrop module consist of a base class called Data and will contain functions that observe outliers and assist removal of outliers in a `DataFrame`
    * `__inti__` takes two parameters a `Pandas Series` and `DataFrame`.
    * function `Outliers()` calculates outliers from the parameter series in the Data object.
        * The forumla for calculating outliers uses interquartile range to create upper and lower bounds
        * The `Outliers()` function returns the index where the outliers are located in the `Dataframe` and the outliers itself 
* The OutlierDrop module also consists of a child class object Dropped.
    * This object takes in the same parameters as Data class, but adds an additional parameter called `threshhold`. The `threshhold` parameter takes a default value of 10 and it represents the maximum amount of outliers that can be dropped in the `Dropped` class. 
    * function `DroppOutliers()` inherits the `Outliers()` function from Data class and uses it to drop the rows of the `Dataframe` that consists of the outliers observed using the `Outliers()` function, within the threshold. 
    
### training module
* The Training module consist of a base class called TrainingData
    * `__init__` takes two parameters a `Pandas DataFrame` and a training `percentage`
        * The `percentage` parameter essentialy is the percentage of training data in the `Dataframe`. The parameter takes a default of 0.5 indicating 50% training and 50% hold out/testing.
    * function `SplitTrain` uses a function imported from pandas to randomly shuffle the entire dataset, and split the `Dataframe` into a training and holdout set based on the given percentage input.
        * function returns a tuple of two `Dataframes`, which are the training and holdout data set.

### anonymizer Module

* This module consists of two classes `AttrIdentifier` and `Anonymizer`. 
    * `AttrIdentifier`: This is the base class used in this subpackage. The base class is added with an idea to includes general information about the Pseudonymizer subpackage. The class provides a default classification of some of the commonly occurring data such as name, date of birth, address and zipcode. It also exposes methods to be able to explicitly set the list of identifiers when the user does not want to use the default classification. 
        * `suggest()`: Function looks at a standard list of identifier names and provides default classification into types Explicit identifier, Quasi identifier, Sensitive identifier and Other identifier. The user can provide their own list of identifier classification to override the default classification provided by the suggest function. 
            * `input`: list of dataset column names.
            * `return`: A dictionary containing the classification of those column names into the classification types mentioned above.
    * `Anonymizer`: `Anonymizer` class is a child class inherited from the `AttrIdentifier`class. It consists of a function `kcounter`. 
        * `kcounter()`: This function can identify the minimum number of k-anonymized records in a given dataset. This number is called the k-value of a dataset. If this number is lower than desired there is a need to further anonymize the dataset to increase the k-value that is satisfactory. This function can be the starting point of the anonymization process. 
            * `input`: Dataframe containing the dataset. 
                    List of quasi identifier columns 
            * `return`: k-value (`int`)

### evaluator Module

* `Ldiversity`: This module contains a class `Ldiversity`, which inherits from the `AttrIdentifier` class in the `Anonymizer` module. The class has a function `ldivMaxProb`.
    * `ldivMaxProb()`: The function looks at a dataset and identifies the distinct values of the sensitive information in the dataset among the k-anonymized group. 
        * `input`:  Dataset, List of Quasi-identifiers, and List of sensitive identifiers 
        * `return`: The Maximum probability of identifying the owner of the sensitive data (`float`)

