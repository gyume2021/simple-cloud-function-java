import sys

from pyspark.sql import SparkSession


def lower_clean_str(x):
    punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”’‘—'
    lowercased_str = x.lower()
    for ch in punc:
        lowercased_str = lowercased_str.replace(ch, '')
    return lowercased_str

if len(sys.argv) != 3:
    raise Exception("Please provide 2 inputs: <gcs_input_file> <gcs_output_directory>")
input_file = sys.argv[1]
output_dir = sys.argv[2]

print(f"Getting source data from {input_file}")
sc = SparkSession.builder.appName('wordcount').getOrCreate()
text_file = sc.sparkContext.textFile(input_file)  # Read the text file
text_file_remove_punct_lower_case = text_file.map(
    lower_clean_str)  # Lowercase all the capital letter and remove punctuations
lines = text_file_remove_punct_lower_case.flatMap(lambda line: line.split())  # Split the word by empty space
pairs = lines.map(lambda s: (s, 1))  # Count occurrence of each word (e.g. 'hello':1)
counts = pairs.reduceByKey(
    lambda accumulation, current: accumulation + current)  # Sum all the occurrence of each unique word
df = counts.toDF(["word", "count"])  # Convert rdd to dataframe
# Remove _SUCCESS file by setting the option to False
print(f"Writing to {output_dir}")
df.coalesce(1).write.mode("overwrite").option("header",True).option("mapreduce.fileoutputcommitter.marksuccessfuljobs", False).csv(
    output_dir)