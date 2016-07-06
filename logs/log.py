#!/usr/bin/env python3

import json
import re
import math
import random
import collections
import datetime

def remove_comments(string):
    return re.sub(r"//.*?\n", "\n", string)

class LogGenerator:
    def __init__(self):
        self.data = None
        self.template = None

    def load(self, filename):
        datastr = remove_comments(open(filename).read())
        self.data = json.loads(datastr)
        return self.data

    def __generate_single(self, d):
        number = random.random() * sum(d.values())
        for k,v in d.items():
            if number < v:
                break
            number -= v
        return k

    def __generate(self, eps, var):
        vals = var['vals']
        nums = len(vals)
        d = {}
        for val in vals:
            d[val['val']] = val['weight']
        return [ self.__generate_single(d) for i in range(eps) ]

    def __generate_bytes(self, var):
        return random.randint(var['start'], var['end'])

    def generate(self, template):
        self.template = template['template']
        start = self.data['start']
        end = self.data['end']
        #eps = template['eps']
        eps = 10
        data = {'byte' : [], 'src_ip' : [], 'dest_ip' : [], 'code' : [], 'method' : [], 'date' : [], 'bytes' : [], 'url' : []}
        variables = template['vars']
        for var in variables:
            if var['name'] == "bytes":
                data['bytes'] = [ self.__generate_bytes(var) for i in range(eps) ]
            elif var['name'] == 'date' or var['name'] == 'dest_ip':
                continue
            else:
                data[var['name']] = self.__generate(eps, var)
        return data

    def __substitute(self, data):
        tosub = ''
        t = self.template[:]
        for key in data:
            t = re.sub(r"<%{}%>".format(key), str(data[key]), t)
        return t
    
    def generate_log(self, data):
        src_ip = data['src_ip']
        code = data['code']
        method = data['method']
        byte = data['bytes']
        n = len(src_ip)
        logs = []
        for i in range(n):
            #log = "{} {} {} {}".format(src_ip[i], method[i], code[i], byte[i])
            log = {'src_ip' : src_ip[i], 'method' : method[i], 'code' : code[i], 'bytes' : byte[i] }
            l = self.__substitute(log)
            logs.append(l)
        return logs

def main():
    generator = LogGenerator()
    data = generator.load( "../data/logscript/ssh_brute_force_apache.json")
    generated = generator.generate(generator.data['templates'][0])
    logs = generator.generate_log(generated)
    print('\n'.join(logs))

if __name__ == "__main__":
    main()

