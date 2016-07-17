#!/usr/bin/env python3

import json
import random
import datetime

from log import remove_comments
from models import Ticket, Update, db_connect, DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

class LogDB:
    def __init__(self):
        self.data = None
        self.start = 0
        self.end = 0

    def load(self, filename):
        datastr = remove_comments(open(filename).read())
        self.data = json.loads(datastr)
        self.start = float(self.data['start'])
        self.end = float(self.data['end'])
        return self.data

    def __generate_val(self, d):
        number = random.random() * sum(d.values())
        for k,v in d.items():
            if number < v:
                break
            number -= v
        return k

    def __generate(self, var):
        vals = var['vals']
        nums = len(vals)
        d = {}
        for val in vals:
            d[val['val']] = val['weight']
        return self.__generate_val(d)

    def generate_event(self):
        events = self.data['transactions'][0]['events']
        event = events[0]
        vari = event['vars']
        data = {}
        for var in vari:
            try:
                val = ''
                if var['type'] == 'standard':
                    val = self.__generate(var)
                if var['type'] == 'increment':
                    db = DBHandler()
                    val = db.ls_increment('ticket', value=str(var['start']))
                data[var['name']] = val
            except KeyError:
                continue
        return data

    def generate_event_many(self):
        events = self.data['transactions'][0]['events'][0]
        while self.start <= self.end:
            datalist = []
            repeat = events['repeat']
            repeat = random.randint(repeat['lowest'], repeat['highest'])
            delay_before = events['delay_before']
            delay_before = random.randint(delay_before['lowest'], delay_before['highest'])
            delay = events['delay']
            delay = random.uniform(delay['lowest'], delay['highest'])
            self.start += delay_before
            for i in range(repeat):
                d = self.generate_event()
                d['timestamp'] = self.start
                datalist.append(d)
            yield datalist
            self.start += delay

class DBHandler:
    def __init__(self):
        self.data = None

    def createdb(self):
        engine = db_connect()
        DeclarativeBase.metadata.create_all(engine)

    def insert_all(self, model):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        mapper = inspect(model)
        attr_names = [c_attr.key for c_attr in mapper.mapper.column_attrs]

        for dictionary in self.data:
            tup = tuple()
            d = {}
            for attr in attr_names:
                try:
                    d[attr] = str(dictionary[attr])
                except KeyError:
                    d[attr] = ''
            datum = model(**d)
            session.add(datum)
        session.commit()
        session.close()

    def query_single(self, model, d):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        data = session.query(model).filter_by(**d)
        self.__display(data)

    def query_all(self, model):
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        m = session.query(model).all()
        self.__display(m)

    def ls_increment(self, filename="ticket", value=None):
        val = None
        try:
            val = open(filename, 'r').read()
            if val:
                with open(filename, 'w') as f:
                    val = int(val)
                    val +=1 
                    f.write(str(val))
            else:
                with open(filename, 'w') as f:
                    f.write(value)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                f.write(value)
                val = value
        return val

    def __display(self, data):
        print('-' * 30)
        for d in data:
            print(d.__dict__)
            print('=' * 50)
        print('-' * 30)
        print("Total rows : ", len(list(data)))

def main():
    logfile = '../data/logscript/logdb'
    with open(logfile, 'w') as f:
        generator = LogDB()
        generator.load( "../data/logscript/mysql_entries.json")
        data = generator.generate_event()
        for datalist in generator.generate_event_many():
            db = DBHandler()
            db.createdb()
            db.data = datalist
            db.insert_all(Ticket)
        #db.query_single(Ticket,  {"ticket" : "1000" })
        #db.query_all(Ticket)

if __name__ == "__main__":
    main()

