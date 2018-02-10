import sys

# Input/Output
source = open(sys.argv[1], "r")
percentile = open(sys.argv[2], "r")
destination = open(sys.argv[3], "w")

def read_from_source(source):
    campaign_contributions = source.read()

def write_to_destination(record, destination):
    destination.write("|".join(record) + "\n")
