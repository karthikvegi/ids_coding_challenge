import sys
from datetime import datetime

# Input/Output
source = open(sys.argv[1], "r")
percentile = open(sys.argv[2], "r")
destination = open(sys.argv[3], "w")

campaign_data = []

def read_from_source(source):
    global campaign_data
    campaign_data = source.read()

def write_to_destination(record, destination):
    destination.write("|".join(record) + "\n")

def empty_fields(fields):
    if any(map(lambda x: not x.strip(), fields)):
        return True

def malformed_field(field, ideal_length):
    if len(field) < ideal_length:
        return True

def invalid_date(field, format):
    try:
        datetime.strptime(field, format)
    except Exception as e:
        return True
