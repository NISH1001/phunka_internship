#!/usr/bin/env python3

import requests
import zipfile, gzip
import io
import os
import glob
import json
import shutil
import tempfile

from sqlalchemy import inspect

from models import *


#datetime.date.today().strftime("%Y%m%d")


class ManualError(Exception):
    def __init__(self, args):
        self.args = args

    def display(self):
        print(''.join(self.args))

class AmplitudeClass:
    def __init__(self, api_key, secret_key, start, end):
        self.path = "../data/amplitude/"
        self.api_key = api_key
        self.secret_key = secret_key
        self.start = start
        self.end = end
        self.url = "https://amplitude.com/api/2/export?start={}T5&end={}T20".format(start, end)
        self.response = None
        self.data = []

    # get method -> return the status code
    def get_response(self):
        self.response = requests.get(self.url, auth=(self.api_key, self.secret_key) )
        return self.response.status_code

    def extract(self):
        try:
            if self.response.status_code != 200:
                raise ManualError("lol.. retard response...")

            # extract the root zip and rename it according to start-end dates
            zips = zipfile.ZipFile(io.BytesIO(self.response.content))
            path = self.get_current_path()
            zips.extractall(self.path)
            root_zip = zips.namelist()[0].split('/')[0]
            shutil.move(self.path + root_zip, self.get_current_path())

            path = self.get_current_path()
            files = os.listdir(self.get_current_path())
            #files = glob.glob(self.get_current_path())
            for fname in files:
                self._extract(path, fname)
                os.remove(path + fname)

        except ManualError as merr:
            merr.display()
            return False
        return True

    def _extract(self, path,  filename):
        total_path = path + filename
        print(total_path)
        gzfile = gzip.open(total_path, 'rb')
        outfname = filename.split(".")[:-1]
        outfile = open(path + '.'.join(outfname), 'wb')
        outfile.write(gzfile.read())
        gzfile.close()
        outfile.close()


    # read single file
    def _read_json(self, filename):
        data = [json.loads(line) for line in  open(filename) ]
        return data
    
    def read_json_all(self, path):
        files = os.listdir(path)
        dicts = []
        for f in files:
            if "json" in f:
                filename = path + f
                data = self._read_json(filename)
                dicts += data
        self.data = dicts
        return dicts

    def createdb(self):
        engine = db_connect()
        DeclarativeBase.metadata.create_all(engine)

    def insert_all(self):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        mapper = inspect(Amplitude)
        attr_names = [c_attr.key for c_attr in mapper.mapper.column_attrs]

        for dictionary in self.data:
            tup = tuple()
            d = {}
            for attr in attr_names:
                try:
                    d[attr] = str(dictionary[attr])
                    #print(type(d[attr]), attr,  d[attr])
                except KeyError:
                    d[attr] = ''
            amp = Amplitude(**d)
            print(amp)
            session.add(amp)
        session.commit()
        session.close()

    def query_all(self):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        amps = session.query(Amplitude).all()
        self.__display(amps)

    def query_single(self, d):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        amps = session.query(Amplitude).filter_by(**d)
        self.__display(amps)

    def __display(self, amps):
        for amp in amps:
            print(amp.__dict__)
            print('=' * 50)
        print('-' * 30)
        print("Total rows : ", len(list(amps)))

    def get_current_path(self):
        return self.path + self.start + "-" + self.end + "/"
    
def main():
    pass

if __name__ == "__main__":
    main()

