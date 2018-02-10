import sys
from datetime import datetime

# Input/Output
source = open(sys.argv[1], "r")
percentile = open(sys.argv[2], "r")
destination = open(sys.argv[3], "w")

def read_from_source(source):
    campaign_contributions = source.read()

def write_to_destination(record, destination):
    destination.write("|".join(record) + "\n")

def invalid_fields(record):
    fields = record.split("|")
    # Check empty fields
    if any(map(lambda x: not x.strip(), fields)):
        return True
    if len(fields[2].strip()) < 5:
        return True
    try:
        datetime.strptime(fields[3], '%m%d%Y')
    except Exception as e:
        return True
