#!/usr/bin/python
import sys
import random

lat_bound = [-74.257159, -73.699215]
long_bound = [40.495992, 40.915568]

with open('clusters.txt', 'w') as f:
  for c in range(int(sys.argv[1])):
    lat = random.uniform(lat_bound[0], lat_bound[1])
    lon = random.uniform(long_bound[0], long_bound[1])
    f.write(str(c)+','+str(0)+','+str(lat)+','+str(lon)+'\n')
