from mrjob.job import MRJob
import math

class KMeans(MRJob):
  """
  Map reduce job to perform one iteration of KMeans clustering
  Euclidean distance is used for measuering similarity
  Centroids are read from input file provided
  """

  def get_nearest_cluster(self, point, centroids):
    """
    Compute the distance of point from all the centroids
    and return the centroid id of nearest centroid.
    """
    distance = float('inf')
    nearest = None
    for centroid in centroids:
      dist = math.sqrt(math.pow(point[0] - centroid[1], 2) + math.pow(point[1] - centroid[2], 2))
      if dist < distance:
        distance = dist
        nearest = centroid[0]
    return nearest

  def read_centroids(self, filename):
    """
    Return a list of centroids by their centroid id and coordinates
    """
    clusters = []
    cluster_file = open(filename, 'r')
    cluster_data = cluster_file.read()
    cluster_file.close()
    del cluster_file

    for line in cluster_data.strip().split('\n'):
      try:
        cluster_id, latitude, longitude = line.split(',')
        clusters.append((cluster_id, float(latitude), float(longitude)))
      except ValueError:
        print('Unable to read clusters file correctly')
    return clusters
    
  def mapper(self, _, line):
    """
    Read coordinates of points and find the nearest cluster. Ouput in the following format
    nearest_cluster_id  point_x point_y
    """
    filename = 'clusters.txt'
    centroids = self.read_centroids(filename)
    row_data = line.strip().split(',')
    try:
      # Reading the lat,lon of the start of the trips
      start_location = [float(row_data[5]), float(row_data[6])]
    except:
      pass
    else:
      nearest_cluster_id = self.get_nearest_cluster(start_location, centroids)
      yield nearest_cluster_id, start_location
  
  def reducer(self, key, points):
    """
    Reducer job reads cluster_id and data point and returns the recomputed value of the centroid
    """
    sum_lat = 0
    sum_lon = 0
    count = 0
    for point in points:
      count += 1
      sum_lat += point[0]
      sum_lon += point[1]
    print(str(key) + ',' + str(sum_lat/count) + ',' + str(sum_lon/count))


if __name__ == '__main__':
  KMeans.run()