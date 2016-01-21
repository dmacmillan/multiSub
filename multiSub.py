import subprocess
from Queue import Queue
from threading import Thread
import argparse, os, sys, re

parser = argparse.ArgumentParser(description='Given a list of commands to run, thread the commands to run concurrently defined by number of threads specified.')
parser.add_argument('commands', help='File containing bash commands to run, one command per line.')
parser.add_argument('-t', '--threads', type=int, default=2, help='Number of commands to run concurrently. Default is 2.')

args = parser.parse_args()

# Some global variables
q = Queue()

def parseCommands(commands):
    with open(commands,'r') as f:
       return [x.strip().split() for x in f.readlines()]

commands = parseCommands(args.commands)

def run(command):
    print 'Running command: {}'.format((' ').join(command))
    subprocess.check_call(command)
    print 'DONE'

def worker(q):
    for args in iter(q.get, None):
        try:
            run(args)
        except Exception as e:
            print '{} failed: {}'.format(args, e)

for command in commands:
    q.put(command)

for i in range(args.threads):
    t = Thread(target = worker, args = (q, ))
    t.setDaemon(True)
    t.start()

q.join()
