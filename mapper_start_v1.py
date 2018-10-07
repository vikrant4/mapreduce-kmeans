import math
import sys

# Store the cluster_id, latitude, longitude
clusters = []

def get_clusters():
  """
  Read initial clusters from clusters.txt
  """
  cluster_file = open('clusters.txt', 'r')
  cluster_data = cluster_file.read()
  cluster_file.close()
  del cluster_file

  # Now convert the data into clusters
  for line in cluster_data.strip().split('\n'):
    try:
      cluster_id, latitude, longitude = line.split(',')
      clusters.append((cluster_id, float(latitude), float(longitude)))
    except ValueError:
      continue


def get_euclidean_distance(lat1, long1, lat2, long2):
  """
  Find Euclidean distance between two coordinates
  """
  distance = math.sqrt(math.pow(lat1 - lat2,2) + math.pow(long1 - long2,2))
  return distance

def get_nearest_cluster(latitude, longitude):
  """
  Return nearest cluster id based on the coordinates
  List of clusters is read using get_clusters() method and stored in clusters variable
  """
  nearest_cluster_id = None
  nearest_cluster_distance = float('inf')
  for cluster in clusters:
    dist = get_euclidean_distance(cluster[1], cluster[2], latitude, longitude)
    if dist < nearest_cluster_distance:
      nearest_cluster_id = cluster[0]
      nearest_cluster_distance = dist
  return nearest_cluster_id

# Begining of the program

# First we get the data for initial clusters
get_clusters()

# lat_bound = [-74.257159, -73.699215]
# long_bound = [40.495992, 40.915568]

# Now we start reading data points and emit the points along with their nearest cluster_id
for line in sys.stdin:
  line = line.strip()
  row = line.split(',')


  # If the length of the data is not valid, move to next iteration
  if len(row) != 18:
    continue
  
  try:
    start_location = [float(row[5]), float(row[6])]
    # end_location = [float(row[9]), float(row[10])]
  except ValueError:
    continue
  
  # Filtetring the trips outside nyc
  # if (start_location[0] < lat_bound[0]) | (start_location[0] > lat_bound[1]):
  #   continue
  # if (start_location[1] < long_bound[0]) | (start_location[1] > long_bound[1]):
  #   continue
  
  # Find the nearest cluster for valid data
  nearest_cluster_id = get_nearest_cluster(start_location[0], start_location[1])
  print(str(nearest_cluster_id) + ' ' + str(start_location[0]) + ' ' + str(start_location[1]))
  # print(str(nearest_cluster_id) + ' ' + str(end_location[0]) + ' ' + str(end_location[1]))
