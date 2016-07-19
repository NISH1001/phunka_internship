#!/usr/bin/env python3

import sys

from log import LogGenerator
from db import LogDB, DBHandler
from models import Ticket, Update

def gen_apache(jsonfile, logfile, dump=False):
    with open(logfile, 'w') as f:
        generator = LogGenerator()
        data = generator.load(jsonfile)
        for event in generator.generate_eps(data['templates'][0]):
            logs = generator.generate_log(event)
            logstr = '\n'.join(logs)
            print(logstr)
            if dump:
                f.write(logstr+'\n')

def gen_auth(jsonfile, logfile, dump=False):
    with open(logfile, 'w') as f:
        generator = LogGenerator()
        data = generator.load(jsonfile)
        events = data['transactions'][0]['events']
        for event in events:
            generator.set_event(event)
            for logs in generator.generate_transaction_all(data['transactions'][0]):
                logstr = '\n'.join(logs)
                print(logstr.strip())
                if dump:
                    f.write(logstr+'\n')

def gen_sql(jsonfile, dump=False):
    generator = LogDB()
    generator.load(jsonfile)
    #events = generator.data['transactions'][0]['events']
    for datalist in generator.generate_event_many(generator.events[0]):
        if dump:
            print("... dumping to db : tickets Table")
            db = DBHandler()
            db.createdb()
            db.data = datalist
            db.insert_all(Ticket)
        else:
            print(datalist)

    for datalist in generator.generate_event_many(generator.events[1]):
        if dump:
            print("... dumping to db : updates table")
            db = DBHandler()
            db.createdb()
            db.data = datalist
            db.insert_all(Update)
        else:
            print(datalist)

def main():
    try:
        arg = sys.argv[1]
        dump = False if "--dump" not in sys.argv else True
        if arg == "--apache":
            jsonfile = "../data/logscript/ssh_brute_force_apache.json"
            logfile = '../data/logscript/apache.log'
            gen_apache(jsonfile, logfile, dump)
        elif arg == "--ssh":
            jsonfile = "../data/logscript/ssh_brute_force_apache.json"
            logfile = '../data/logscript/auth.log'
            gen_auth(jsonfile, logfile, dump)
        elif arg == "--mysql":
            jsonfile = "../data/logscript/mysql_entries.json"
            gen_sql(jsonfile, dump)
        else:
            print("Use --apache or --ssh or --mysql")
            print("Use --dump to write to file or database")
    except IndexError:
            print("Use --apache or --ssh or --mysql as parameters")
            print("Use --dump to write to file or database")



if __name__ == "__main__":
    main()

