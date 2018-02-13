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

def valid_record(record):
    zip_code = record[2]
    transaction_dt = record[3]
    if not empty_fields(record) \
            and not malformed_field(zip_code, 5) \
            and not invalid_date(transaction_dt, '%m%d%Y'):
        return True

def ingest_record(row):
    fields = row.split("|")
    other_id = fields[15]
    record = [fields[0], fields[7], fields[10][:5], fields[13], fields[14]]
    # Process only individual contributions and valid records
    if other_id.strip() == "" and valid_record(record):
        return record

def process_data(source, destination, percentile):
    campaign_data = source.read()
    valid_records = invalid_records = 0
    # Data Structures
    donor_list = {} # Key: donor_id | Value: transaction_yr
    donation_dict = defaultdict(list) # Key: recipient | Value: list of transactions

    for row in campaign_data.splitlines():
        record = ingest_record(row)
        if not record:
            invalid_records += 1
            continue
        valid_records += 1
        recipient, donor, zip_code, transaction_dt, transaction_amt = record
        transaction_yr = int(transaction_dt[4:])
        transaction_amt = int(round(float(transaction_amt)))
        donor_id = "-".join([donor, zip_code])
        recipient_id = "-".join([recipient, zip_code, str(transaction_yr)])

        # New donor
        if donor_id not in donor_list:
            donor_list[donor_id] = transaction_yr
        # Repeat donor
        # update transaction_yr if you come across donation from a previous year
        elif transaction_yr < donor_list[donor_id]:
            donor_list[donor_id] = transaction_yr
        # perform calculations
        elif transaction_yr > donor_list[donor_id]:
            # Accumulate contributions as a list in the dictionary
            donation_dict[recipient_id].append(transaction_amt)
            transaction_cnt = len(donation_dict[recipient_id])
            contribution = sum(donation_dict[recipient_id])
            running_percentile = compute_percentile(donation_dict[recipient_id], percentile)

            output = [recipient, zip_code, str(transaction_yr), str(running_percentile), str(contribution), str(transaction_cnt)]
            write_to_destination(output, destination, '|')
    print_summary_statistics([valid_records, invalid_records])

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

    process_data(source, destination, percentile)
    clean_up()
