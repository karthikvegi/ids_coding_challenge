#-------------------------------------------------------------------------------
# Author: Karthik Vegi
# Email: karthikvegi@outlook.com
# Python Version: 3.6
#-------------------------------------------------------------------------------
import sys
import math
from utils import *
from collections import defaultdict

def clean_up():
    source.close()
    destination.close()
    percentile_source.close()

def ingest_record(row):
    cols = row.split("|")
    other_id = cols[15]
    fields = [cols[0], cols[7], cols[10][:5], cols[13], cols[14]]
    record = {}
    # Process only individual contributions and valid records
    if other_id.strip() == "" and valid_record(fields):
        # Create a dictionary with fields for easy access
        record['recipient'] = cols[0]
        record['donor'] = cols[7]
        record['zip_code'] = cols[10][:5]
        record['transaction_yr'] = int(cols[13][4:])
        record['transaction_amt'] = int(cols[14])
        record['donor_id'] = record['donor'] + record['zip_code']
        record['recipient_id'] = record['recipient'] + record['zip_code'] + str(record['transaction_yr'])
        return record

def valid_record(record):
    zip_code = record[2]
    transaction_dt = record[3]
    if not empty_fields(record) \
            and not malformed_field(zip_code, 5) \
            and not invalid_date(transaction_dt, '%m%d%Y'):
        return True

def process_data(source, destination):
    # Data Structures
    donor_dict = {} # Key: donor_id | Value: transaction_yr
    donation_dict = defaultdict(list) # Key: recipient | Value: list of transactions
    for row in source.read().splitlines():
        record = ingest_record(row)
        if not record:
            continue
        # New donor
        if record['donor_id'] not in donor_dict:
            donor_dict[record['donor_id']] = record['transaction_yr']
        # update transaction_yr if you come across donation from a previous year
        elif record['transaction_yr'] < donor_dict[record['donor_id']]:
            donor_dict[record['donor_id']] = record['transaction_yr']
        elif record['transaction_yr'] > donor_dict[record['donor_id']]:
            # Accumulate contributions as a list in the dictionary
            donation_dict[record['recipient_id']].append(record['transaction_amt'])
            transaction_cnt = len(donation_dict[record['recipient_id']])
            contribution = sum(donation_dict[record['recipient_id']])
            pct = compute_percentile(donation_dict[record['recipient_id']], percentile)
            output = [record['recipient'], record['zip_code'], str(record['transaction_yr']), str(pct), str(contribution), str(transaction_cnt)]
            write_to_destination(output, destination, '|')

if __name__ == "__main__":
    try:
        if len(sys.argv) < 4:
            raise Exception("Missing args! Correct Usage: <program.py> <inp_file> <pct_file> <out_file>")
        source = open(sys.argv[1], "r")
        destination = open(sys.argv[3], "w")
        percentile_source = open(sys.argv[2], "r")
        percentile = float(percentile_source.read())
        if  percentile < 0 or percentile > 100:
            raise ValueError("Invalid Percentile: Percentile value should between 1 to 100")
    except Exception as e:
        print(e)
        sys.exit(1)
    process_data(source, destination)
    clean_up()
