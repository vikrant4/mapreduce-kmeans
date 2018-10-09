#!/usr/bin/python
import sys

current_cluster = None
current_distance = 0
current_count = 0

for line in sys.stdin:
  line = line.strip()
  cluster, distance = line.split('\t')

  if cluster == current_cluster:
    current_count += 1
    current_distance += float(distance)
  else:
    print(current_cluster + '\t' + str(current_distance) + ' ' + str(current_count))
    current_cluster = cluster
    current_count = 1
    current_distance = float(distance)

print(current_cluster + '\t' + str(current_distance) + ' ' + str(current_count))