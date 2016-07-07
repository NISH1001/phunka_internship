#!/usr/bin/env python3

from log import LogGenerator

def main():
    logfile = '../data/logscript/log'
    generator = LogGenerator()
    data = generator.load( "../data/logscript/ssh_brute_force_apache.json")
    #generated = generator.generate(generator.data['templates'][0])
    with open(logfile, 'w') as f:
        for event in generator.generate_eps(data['templates'][0]):
        #for event in generator.generate_eps(data['transactions'][0]['events'][0]):
            logs = generator.generate_log(event)
            logstr = '\n'.join(logs)
            print('\n'.join(logs))
            #f.write(logstr+'\n')

if __name__ == "__main__":
    main()

