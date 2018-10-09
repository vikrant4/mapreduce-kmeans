#!/usr/bin/python
import sys

cluster_map = dict()

for line in sys.stdin:
  cluster_id, data = line.strip().split('\t')
  count, latitude, longitude = data.split(' ')
  if cluster_id in cluster_map:
    cluster_map[cluster_id]['count'] += 1
    cluster_map[cluster_id]['sumLat'] += float(latitude)
    cluster_map[cluster_id]['sumLon'] += float(longitude)
  else:
    cluster_map[cluster_id] = {
      'count': float(count),
      'sumLat': float(latitude),
      'sumLon': float(longitude)
    }

for cluster in cluster_map:
  print(cluster + '\t' + str(cluster_map[cluster]['count']) + ' ' + str(cluster_map[cluster]['sumLat']) + ' ' + str(cluster_map[cluster]['sumLon']))