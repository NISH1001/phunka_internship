#!/usr/bin/env python3

import json
import re
import math
import random
import collections
import datetime

# helper to remove comments for non-standard JSON file
def remove_comments(string):
    return re.sub(r"//.*?\n", "\n", string)

"""
    LogGenerator class
    - parses the format
    - generates log on the basis of eps (events per seconds)
"""
class LogGenerator:
    def __init__(self):
        self.data = None
        self.template = None
        self.event = []
        self.eps = None
        self.start = 0
        self.end = 0

    # load the JSON file
    def load(self, filename):
        datastr = remove_comments(open(filename).read())
        self.data = json.loads(datastr)
        return self.data

    # generate single value based on weighted distribution
    def __generate_single(self, d):
        number = random.random() * sum(d.values())
        for k,v in d.items():
            if number < v:
                break
            number -= v
        return k

    # generate eps no. of values
    def __generate(self, eps, var):
        vals = var['vals']
        nums = len(vals)
        d = {}
        for val in vals:
            d[val['val']] = val['weight']
        return [ self.__generate_single(d) for i in range(eps) ]

    # generate random byte
    def __generate_random(self, var):
        return random.randint(var['start'], var['end'])

    # generate eps no. of event per second -> for apache log
    def generate(self, template):
        self.template = template['template']
        data = {}
        variables = template['vars']
        eps = template['eps']
        self.eps = eps
        self.event_counter = eps
        for var in variables:
            if var['type'] == "random_number":
                data[var['name']] = [ self.__generate_random(var) for i in range(eps) ]
            elif var['name'] == 'dest_ip':
                continue
            elif var['type'] == 'datetime':
                data['time_format'] =  var['format']
            elif var['type'] == "standard":
                data[var['name']] = self.__generate(eps, var)
            else:
                continue
        return data

    # set a specific event
    def set_event(self, event):
        self.event = event

    #for single transaction
    def generate_transaction_single(self, transaction):
        template = self.event
        self.template = self.event['template']
        repeat = template['repeat']
        repeat = random.randint(repeat['lowest'], repeat['highest'])
        delay_before = template['delay_before']
        delay_before = random.randint(delay_before['lowest'], delay_before['highest'])
        delay = template['delay']
        delay = random.uniform(delay['lowest'], delay['highest'])
        data = {}
        variables = template['vars']
        for var in variables:
            if var['type'] == "random_number":
                data[var['name']] = self.__generate_random(var)
            elif var['name'] == 'dest_ip':
                continue
            elif var['type'] == 'datetime':
                data['time_format'] =  var['format']
            elif var['type'] == "standard":
                data[var['name']] = self.__generate(1, var)[0]
            else:
                continue
        return {'data' : data, 'delay' : delay, 'delay_before' : delay_before, 'repeat' : repeat}

    # for transactions
    def generate_transaction_all(self, transaction):
        start = self.data['start']
        end = self.data['end']
        event = {}
        while start <= end:
            single = self.generate_transaction_single(transaction)
            start += single['delay_before']
            data = single['data']
            date = datetime.datetime.fromtimestamp(start).strftime(data['time_format'])
            data['date'] = date
            del data['time_format']
            log = self.__substitute(data)
            logs = [ log for i in range(single['repeat']) ]
            yield logs
            start += single['delay']

    # generate n event values per second in a given specific timestamp
    # this function is used for apache log only
    def generate_eps(self, template):
        start = self.data['start']
        end = self.data['end']
        event = {}
        while start <= end:
            data = self.generate(template)
            event['data'] = data
            date = datetime.datetime.fromtimestamp(start).strftime(data['time_format'])
            del data['time_format']
            event['date'] = date.strip()
            yield event
            start += 1

    # fill the log format with data
    def __substitute(self, data):
        tosub = ''
        t = self.template[:]
        for key in data:
            t = re.sub(r"<%{}%>".format(key), str(data[key]), t)
        return t
    
    # finally generate the log with loging format specified -> for apache logs
    def generate_log(self, event):
        data = event['data']
        """
        src_ip = data['src_ip']
        code = data['code']
        method = data['method']
        byte = data['bytes']
        """
        #n = len(src_ip)
        n = self.eps
        logs = []
        for i in range(n):
            log = { key : data[key][i] for key in data }
            log['date'] = event['date']
            #log = {'src_ip' : src_ip[i], 'method' : method[i], 'code' : code[i], 'bytes' : byte[i], 'date' : event['date'] }
            logs.append(self.__substitute(log))
        return logs

def main():
    pass

if __name__ == "__main__":
    main()

