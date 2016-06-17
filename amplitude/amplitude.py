#!/usr/bin/env python3

import requests
import zipfile
import io
import os
import glob
import json
import shutil
import tempfile

from models import *
from sqlalchemy import inspect

API_KEY = "e6166c7b0b4702b98e06035087ceec57"
SECRET_KEY = "0d3b7d2c3df2d4cebe39bb2a900dfae7"

class ManualError(Exception):
    def __init__(self, args):
        self.args = args

    def display(self):
        print(''.join(self.args))

class AmplitudeClass:
    def __init__(self, api_key, secret_key, start, end):
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = "https://amplitude.com/api/2/export?start={}T5&end={}T20".format(start, end)
        self.response = None
        self.data = []

    # get method -> return the status code
    def get_response(self):
        self.response = requests.get(self.url, auth=(self.api_key, self.secret_key) )
        return self.response.status_code

    """
    def extract(self):
        try:
            if self.response.status_code != 200:
                raise ManualError("lol.. retard response...")

            zips = zipfile.ZipFile(io.BytesIO(self.response.content))
            zips.extractall("./data/")
            for z in zips.namelist():
                dirname = os.path.splitext(z)[0]
                jsonname = dirname.split("/")[1]
                print(jsonname)
                content = zips.read(z)
                zio = io.BytesIO()
                zio.write(content)
                tempzip = zipfile.ZipFile(zio, 'w')
                tempzip.writestr("./data/" + jsonname, zio.getvalue())
                tempzip.extractall()

        except ManualError as merr:
            merr.display()
            return False
        return True
    """

    def extract(self):
        with open("./data/testzip", "wb") as fp:
            fp.write(self.response.content)

    # as for now, recursive unzipping doesn't work :/
    def unzip_recursively(self, parent_archive):
        parent_archive = zipfile.ZipFile(parent_archive)
        result = {}
        tmpdir = tempfile.mkdtemp()
        try:
            parent_archive.extractall(path=tmpdir)
            namelist=parent_archive.namelist()
            for name in namelist[1:]:
                innerzippath = os.path.join(tmpdir, name)
                inner_zip = zipfile.ZipFile(innerzippath)
                inner_extract_path = innerzippath+'.content'
                if not os.path.exists(inner_extract_path):
                    os.makedirs(inner_extract_path)
                inner_zip.extractall(path=inner_extract_path)
    
                for inner_file_name in inner_zip.namelist():
                    result[inner_file_name] = open(os.path.join(inner_extract_path, inner_file_name)).read()
                inner_zip.close()
        finally:
            #shutil.rmtree(tmpdir)
            pass
        return result

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

    
def main():
    amp = AmplitudeClass(API_KEY, SECRET_KEY, "20160610", "20160612")
    #print(amp.get_response())
    #amp.extract()
    #amp.unzip_recursively("./data/testzip")
    #amp.createdb()
    #data = amp.read_json_all("../data/amplitude/")
    #amp.insert_all()
    #amp.query_all()
    amp.query_single( {'uuid':"238f666a-2eca-11e6-b6a6-22000a5981c8"} )

if __name__ == "__main__":
    main()

