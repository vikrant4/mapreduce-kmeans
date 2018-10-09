#!/usr/bin/python
import sys
import subprocess
import os
import math
import random

STREAMING_JAR = '/usr/lib/hadoop-mapreduce/hadoop-streaming.jar'

# Reading options
clusters = int(sys.argv[1])
option = sys.argv[2]
INPUT = sys.argv[3]
OUTPUT = '/user/hadoop/'+option+'_'+clusters

# Randomly creating clusters
print('Creating ' + str(clusters) + ' clusters')
subprocess.call(['python', 'generate_clusters.py', str(clusters)], cwd=option)
iter_count = 0

while True:
  iter_count += 1
  old_cent = dict()
  new_cent = dict()

  print('Iteration: '+str(count))
  # Making the command to run MR job
  command = ['yarn', 'jar', STREAMING_JAR]
  command += ['-mapper', 'mapper.py']
  command += ['-reducer', 'reducer.py']
  command += ['-input', INPUT]
  command += ['-output', OUTPUT]
  command += ['-file', os.getcwd()+'/'+option+'/mapper.py']
  command += ['-file', os.getcwd()+'/'+option+'/reducer.py']
  command += ['-file', os.getcwd()+'/'+option+'/clusters.txt']

  if option == 'combiner':
    command += ['-combiner', 'combiner.py']
    command += ['-file', os.getcwd()+'/'+option+'/combiner.py']

  # Run the command
  subprocess.call(command, cwd=option)

  # Get the result
  output = subprocess.check_output(('hadoop fs -cat '+OUTPUT+'/part*').split(' '))

  # Read old clusters
  with open('./'+option+'/clusters.txt', 'r') as f_in:
    for line in f_in:
      id, count, lat, lon = line.split(',')
      old_cent[id] = {
        'lat': float(lat),
        'lon': float(lon),
        'count': float(count)
      }

  # Read new centroids and write them into clusters.txt
  with open('./'+option+'/clusters.txt', 'w') as f_out:
    for line in output.strip().split('\n'):
      id, count, lat, lon = line.strip().split(' ')
      lat = float(lat)
      lon = float(lon)
      count = float(count)
      new_cent[id] = {
        'lat': lat,
        'lon': lon,
        'count': count
      }
      f_out.write(str(id)+','+str(lat)+','+str(lon)+','+str(count)+'\n')
  
  # Compare the difference
  change = 0

  for cluster in old_cent:
    if cluster not in new_cent:
      new_cent[cluster] = {
        'count': 0,
        'lat': random.uniform(-74.257159, -73.699215),
        'lon': random.uniform(40.495992, 40.915568)
      }
    if new_cent[cluster]['count'] != old_cent[cluster]['count']:
      change = math.fabs(old_cent[cluster]['count'] - new_cent[cluster]['count'])
  
  # Max limit of iterations reached
  if iter_count >= 15:
    break
  
  # Decide if more iterations are required
  if change >=  200:
    break
  else:
    subprocess.call(('hadoop fs -rm -r '+OUTPUT).split(' '))


print('Processing complete, output final output can be found in '+option+'clusters.txt')
  
