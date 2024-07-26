import time, sys, os
from pathlib import Path
from datetime import datetime
import argparse
import findspark

import time
from pyspark.sql import SparkSession, functions as F

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required=True, type=str,
                default='hdfs://localhost:9000/user/train/datasets/market5mil_parquet',
                help="Source file path.")

ap.add_argument("-f", "--format", required=False, type=str, default='csv',
                help="Source file type. Csv, parquet, orc etc.")

ap.add_argument("-head", "--header", required=False, type=bool, default=None,
                help="True if the first line is heade in csv or text source.")

ap.add_argument("-s", "--sep", required=False, type=str, default=',',
                help="Seperator of columns, fields.")

ap.add_argument("-sch", "--inferSchema", required=False, type=bool, default=None,
                help="If True spark infers field type while reading.")

ap.add_argument("-c", "--compression", required=False, type=str, default=None,
                help="File compression types gzip, lzo, snappy")

ap.add_argument("-name", "--appName", required=False, type=str, default="Default App",
                help="Spark Application name")

ap.add_argument("-sh", "--sparkHome", required=False, type=str, default="/opt/spark/",
                help="Spark Application name")

args = vars(ap.parse_args())

input_file = args['input']
file_format = args['format']
header = args['header']
sep = args['sep']
inferSchema = args['inferSchema']
compression = args['compression']
appName = args['appName']
spark_home = args['sparkHome']

findspark.init(spark_home)

# create a SparkSession
spark = SparkSession.builder.appName(appName).getOrCreate()

df = spark.read.format(file_format).option("inferSchema", inferSchema).option("header", header).option("sep", sep).load(
    input_file)

df.select(df.columns[:5]).show()
time.sleep(30)

spark.stop()
