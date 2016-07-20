#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plot

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

class LoanPredict:
    def __init__(self):
        self.model = None

    def load_data(self, filename):
        return pd.read_csv(filename)

    def handle_missing_data(self, dataframe):
        # get missing value stat in the form { 'column_name' : True/False }
        missing_status = dataframe.isnull().any().to_dict()
        print(missing_status)
        
        # now loop over all the columns
        for col in missing_status:
            # check if any missing value
            if missing_status[col]:
                data = dataframe[col]
                groups = dataframe.groupby([col])
                missing_val = None
                if data.dtype == "object":
                    counter = data.value_counts().to_dict()
                    #g = collections.Counter(dataframe[col])
                    missing_val = max(counter, key=counter.get)
                if data.dtype == "float64":
                    missing_val = data.mean()
                # now fill over the null values with missing value
                dataframe[col] = dataframe[col].fillna(missing_val)
        return dataframe

    def remove_columns(self, dataframe, columns):
        df = dataframe
        for col in columns:
            df = df.drop(col, axis=1)
        return df

    def display(self):
        print(dataframe)
        #print(dataframe.columns)
        #print(dataframe.describe())

    def __get_columns_specific(self, dataframe, col_type="categorical"):
        cols = []
        columns = dataframe.columns
        compare = "object" if col_type == "categorical" else "float64"
        for col in columns:
            data = dataframe[col]
            if data.dtype == compare:
                cols.append(col)
            if compare == "float64" and data.dtype=="int64":
                cols.append(col)
        return cols

    def vectorize(self, dataframe, target_col):
        # remove unncecessary columns -> heere loan id is not needed
        train_data = self.remove_columns(dataframe, ['Loan_ID']) 

        # categorical columns
        cat_cols = self.__get_columns_specific(train_data, "categorical")

        # numerical columns
        num_cols = self.__get_columns_specific(train_data, "numerical")

        # vectorize categorical values
        for col in cat_cols:
            number = LabelEncoder()
            train_data[col] = number.fit_transform(train_data[col].astype('str'))

        # vectorize target value too
        if target_col:
            number = LabelEncoder()
            train_data[target_col] = number.fit_transform(train_data[target_col].astype('str'))

        features = list(set(list(train_data.columns)) - {target_col, } )
        return train_data, features

    def train(self, train_data, feature_columns):
        # target column
        target_col = 'Loan_Status'
        #train_data, features = self.vectorize(dataframe, target_col)

        x_train = train_data[feature_columns].values
        y_train = train_data[ target_col ].values
        rf = RandomForestClassifier(n_estimators=1000)
        rf.fit(x_train, y_train)
        self.model = rf

    def predict(self, data, feature_columns):
        x_test = data[feature_columns].values
        final_status = self.model.predict_proba(x_test)
        p = final_status[:, 1]
        print(p)

def main():
    predict = LoanPredict()

    train_data = predict.load_data("../data/loanpredict/train.csv")
    test_data = predict.load_data("../data/loanpredict/test.csv")

    # handle missing data
    train_data = predict.handle_missing_data(train_data)
    test_data = predict.handle_missing_data(test_data)

    train_data, features_cols = predict.vectorize(train_data, "Loan_Status")
    #predict.train_data = train_data
    predict.train(train_data, features_cols)

    test, f = predict.vectorize(test_data, "")
    predict.predict(test, f)


if __name__ == "__main__":
    main()

