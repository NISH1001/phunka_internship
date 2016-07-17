#!/usr/bin/env python3

import json

from log import remove_comments

class LogDB:
    def __init__(self):
        self.data = None
        self.start = 0
        self.end = 0

    def load(self, filename):
        datastr = remove_comments(open(filename).read())
        self.data = json.loads(datastr)
        self.start = self.data['start']
        self.end = self.data['end']
        return self.data


def main():
    logfile = '../data/logscript/logdb'
    with open(logfile, 'w') as f:
        generator = LogDB()
        data = generator.load( "../data/logscript/mysql_entries.json")

if __name__ == "__main__":
    main()

