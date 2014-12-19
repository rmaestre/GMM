#!/opt/spark-1.1.0-bin-hadoop1/bin/pyspark --executor-memory 8G
__author__ = 'roberto'

import sys
import os
import numpy as np
from math import sqrt
import csv
import argparse
from GMMModel import GMMModel

# Global variables
IX_INPUT_FILENAME = "/tmp/bivariate.csv"  # File input
IX_SEPARATOR = ","  # Input line separator
IX_RANGE_TO_CLUSTER = (0, 1)  # Matrix column to be clusterized
IX_FORECAST_VALUE = IX_RANGE_TO_CLUSTER[1] + 0  # Forecast value of each vector


# Set the path for spark installation
os.environ['SPARK_HOME'] = "/opt/spark-1.1.0-bin-hadoop1"
sys.path.append("/opt/spark-1.1.0-bin-hadoop1/python/lib/py4j-0.8.2.1-src.zip")
sys.path.append("/opt/spark-1.1.0-bin-hadoop1/python")

# Import Spark Modules
try:
    from pyspark import SparkContext
    from pyspark import SparkConf
    from pyspark.mllib.clustering import KMeans


except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)


def parseVector(line):
    return np.array([float(x) for x in line.split(',')])


# Setup Spark configuration
conf = SparkConf()
conf.setMaster("local[%s]" % 4)
# conf.setMaster("local")
conf.setAppName("Spark K-Means")
# conf.set("spark.executor.memory", "10g")
#conf.set("spark.eventLog.enabled", "true")
#conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
sc = SparkContext(conf=conf)

"""
Parameters
----------
input_file : path of the file which contains the comma separated integer data points
n_components : Number of mixture components
n_iter : Number of EM iterations to perform. Default to 100
ct : convergence_threshold.Default to 1e-3
"""

input_file = IX_INPUT_FILENAME
lines = sc.textFile(input_file)
data = lines.map(parseVector).cache()

model = GMMModel.trainGMM(data, 2, 100, 10)
responsibility_matrix, cluster_labels = GMMModel.resultPredict(model, data)

# Writing the GMM components to files
means_file = input_file.split(".")[0] + "/tmp/means"
sc.parallelize(model.Means, 1).saveAsTextFile(means_file)

covar_file = input_file.split(".")[0] + "/tmp/covars"
sc.parallelize(model.Covars, 1).saveAsTextFile(covar_file)

responsbilities = input_file.split(".")[0] + "/tmp/responsbilities"
responsibility_matrix.coalesce(1).saveAsTextFile(responsbilities)

cluster_file = input_file.split(".")[0] + "/tmp/clusters"
cluster_labels.coalesce(1).saveAsTextFile(cluster_file)
sc.stop()
