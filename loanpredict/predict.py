#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import random

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

    def vectorize(self, dataframe, unncecessary_cols, target_col):
        # remove unncecessary columns -> heere loan id is not needed
        #train_data = self.remove_columns(dataframe, ['Loan_ID']) 
        train_data = dataframe

        # categorical columns
        cat_cols = list(set(self.__get_columns_specific(train_data, "categorical")) - set(unncecessary_cols))

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

        features = list(set(list(train_data.columns)) - {target_col, } - set(unncecessary_cols) )
        return train_data, features

    def train(self, data, feature_columns, target_column):
        random.seed(100)
        # target column
        #train_data, features = self.vectorize(dataframe, target_col)

        # separte input/output
        x_train = data[feature_columns].values
        y_train = data[ target_column ].values

        # use random forest classifier
        rf = RandomForestClassifier(n_estimators=1000)
        rf.fit(x_train, y_train)
        self.model = rf

    def predict(self, data, feature_columns, target_column, prediction_type="classification"):
        x_test = data[feature_columns].values
        final_status = None
        if prediction_type == "classification":
            final_status = self.model.predict(data[feature_columns])
        else:
            final_status = self.model.predict_proba(x_test)[:, 1]
        return final_status

def main():
    predict = LoanPredict()

    train_data = predict.load_data("../data/loanpredict/train.csv")
    test_data = predict.load_data("../data/loanpredict/test.csv")

    # handle missing data
    train_data = predict.handle_missing_data(train_data)
    test_data = predict.handle_missing_data(test_data)

    train_data['Type'] = 'Train'
    test_data['Type'] = 'Test'
    full_data = pd.concat([train_data, test_data], axis = 0)

    target_column = "Loan_Status"
    unncecessary_cols = ['Loan_ID', 'Type']

    """
    train_data, feature_columns = predict.vectorize(full_data, unncecessary_cols, "Loan_Status")
    print(feature_columns)
    predict.train(train_data, feature_columns)
    """

    # now train the dataset
    data, feature_columns = predict.vectorize(full_data, unncecessary_cols, target_column)
    predict.train(data[data['Type']=='Train'], feature_columns, target_column)

    # now predict using test data
    test = data[data['Type']=='Test']
    p = predict.predict(test, feature_columns, target_column, prediction_type="classification")
    test[target_column] = p
    print(test)

if __name__ == "__main__":
    main()

