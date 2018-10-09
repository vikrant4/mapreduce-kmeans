#!/usr/bin/python
import sys

# cluster _id, count, sum_lat, sum_long
current_cluster = [None, 0, 0, 0]

def add_point(latitude, longitude, current_cluster):
  current_cluster[1] += 1
  current_cluster[2] += float(latitude)
  current_cluster[3] += float(longitude)
  return current_cluster

def emit_centroid(current_cluster):
  """
  Emit the new centroid for cluster and reset the variables for next cluster
  """
  if current_cluster[1] > 0:
    print(str(current_cluster[0]) + ' ' + str(current_cluster[1]) + ' ' + str(current_cluster[2]/current_cluster[1]) + ' ' + str(current_cluster[3]/current_cluster[1]))
  current_cluster = [None, 0, 0, 0]
  return current_cluster

# Start reading the data
for line in sys.stdin:
  line = line.strip()
  cluster_id, point = line.split('\t')
  latitude, longitude = point.split(' ')
  if current_cluster[0] == None:# This is the first line read
    current_cluster[0] = cluster_id
    current_cluster = add_point(latitude, longitude, current_cluster)
  elif current_cluster[0] != cluster_id:
    # All points for the clusters are over, emit the final values and start reading for the new cluster
    current_cluster =  emit_centroid(current_cluster)
    current_cluster[0] = cluster_id
    current_cluster = add_point(latitude, longitude, current_cluster)
  elif current_cluster[0] == cluster_id:
    current_cluster = add_point(latitude, longitude, current_cluster)


# emit data for the last cluster
emit_centroid(current_cluster)