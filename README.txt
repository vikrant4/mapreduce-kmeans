K-means clustering using MapReduce
The code is written in python and uses Hadoop Streaming API to process the data

There are three sub-directories, each runs the kmeans allorithm differently

1. basic
Runs the K-means algorithm without any optimisation with just a mapper and reducer

2. combiner
Runs the K-means algorithm with a with_combiner

3. in-mapper
Runs K-means algorithm with an in-mapper_combiner

Each of the sub-directory has a script generate_clusters.py which randomly generates initial centroids for clusters
using the system arguments and writes them to clusters.txt file. e.g. to run with 3 clusters write command

python generate_clusters.py 3

This will create a clusters.txt with three random centroids (This position of these centoids is bound by the coordinate
boundary of New Your City [https://www1.nyc.gov/assets/planning/download/pdf/data-maps/open-data/nybb_metadata.pdf?ver=18c])

To start the analysis use script.py. This file maanges the K-means iteration and manages the data.
script.py takes 3 command line arguments:

python script.py <no_of_clusters> <option> <input>

no_of_clusters tells how many clusters should kmeans try to find
option tells which sub-directory to use
input dircets to the path of input data realtive to hadoop namenode (Make sure that the input file is already present)