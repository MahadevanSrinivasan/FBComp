import time, csv
import cPickle as pickle

r = csv.reader(open('../Data/train.csv','r'))
r.next()

start_time = time.time()
reversegraph = {}
for edge in r:
    reversegraph.setdefault(edge[1], set()).add(edge[0])
