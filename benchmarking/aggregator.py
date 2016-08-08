#!/usr/bin/env python3

import pandas as pd
import numpy as np


class Aggregator:
    def __init__(self, filename="../data/all_records.csv"):
        self.filename = filename
        self.data = pd.read_csv(filename)
        self.quantiles = {}
        self.q = [0, 0.25, 0.5, 0.75, 0.9]
        self.calculate_quantiles_all()
        self.groups = None

    def calculate_quantiles_all(self):
        q = self.q
        for column in self.data:
            cq = self.get_quantile(self.data, [column], q)
            d = { q[idx] : cq[idx][0]  for idx, x in enumerate(q) }
            d['mean'] = self.data[column].mean()
            self.quantiles[column] = d

    def get_quantile(self, data, columns, quantiles):
        return data[columns].quantile(quantiles).values

    def calculate_quantile_store(self, data, columns, quantiles):
        qs = self.get_quantile(data, columns, self.q)
        return { quantiles[idx] : qs[idx][0] for idx, x in enumerate(qs) }

    def group(self, columns):
        self.groups= self.data.groupby(columns)

    def get_store_data(self, store_tuple):
        return self.groups.get_group(store_tuple)

def main():
    agg = Aggregator(filename="../data/all_records.csv")
    agg.group(columns = ['locationstorenumber', 'paymentyear', 'paymentweeknumber'])
    store = agg.get_store_data( (986, 2016, 2) )
    print(agg.quantiles['ordertotalrevenuesales'])
    print(agg.calculate_quantile_store(store, ['ordertotalrevenuesales'], agg.q))

if __name__ == "__main__":
    main()

