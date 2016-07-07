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
        self.eps = 0

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

    # generate eps no. of event per second
    def generate(self, template):
        self.template = template['template']
        eps = template['eps']
        self.eps = eps
        """
        data = {
                'byte'          : [], 
                'src_ip'        : [], 
                'dest_ip'       : [], 
                'code'          : [], 
                'method'        : [], 
                'date'          : [], 
                'bytes'         : [], 
                'url'           : [], 
                'time_format'   : ''
            }
        """
        data = {}
        variables = template['vars']
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

    # generate n event values per second in a given specific timestamp
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
    
    # finally generate the log with loging format specified
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

