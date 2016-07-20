#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import collections
import operator

class LoanPredict:
    def __init__(self):
        self.train_data = None

    def load_train_data(self, filename):
        self.train_data = pd.read_csv(filename)

    def handle_missing_data(self):
        # get missing value stat in the form { 'column_name' : True/False }
        missing_status = self.train_data.isnull().any().to_dict()
        
        # now loop over all the columns
        for col in missing_status:
            # check if any missing value
            if missing_status[col]:
                data = self.train_data[col]
                groups = self.train_data.groupby([col])
                missing_val = None
                if data.dtype == "object":
                    counter = data.value_counts().to_dict()
                    #g = collections.Counter(self.train_data[col])
                    missing_val = max(counter, key=counter.get)
                if data.dtype == "float64":
                    missing_val = data.mean()
                # now fill over the null values with missing value
                self.train_data[col] = self.train_data[col].fillna(missing_val)

    def display(self):
        print(self.train_data)
        #print(self.train_data.columns)
        #print(self.train_data.describe())

def main():
    predict = LoanPredict()
    predict.load_train_data("../data/loanpredict/train.csv")
    predict.handle_missing_data()

if __name__ == "__main__":
    main()

