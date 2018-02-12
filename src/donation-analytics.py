#-------------------------------------------------------------------------------
# Author: Karthik Vegi
# Email: karthikvegi@outlook.com
# Python Version: 3.6
#-------------------------------------------------------------------------------
import sys
import math
from datetime import datetime
from collections import defaultdict

def write_to_destination(record, destination, delimiter):
    destination.write(delimiter.join(record) + "\n")

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

def valid_record(record):
    zip_code = record[2]
    transaction_dt = record[3]
    if not empty_fields(record) \
            and not malformed_field(zip_code, 5) \
            and not invalid_date(transaction_dt, '%m%d%Y'):
        return True

def compute_percentile(donations, percentile):
    # Nearest-rank method
    donations.sort()
    idx = math.ceil(percentile * 0.01 * len(donations))
    return donations[idx-1]

def ingest_record(row):
    fields = row.split("|")
    other_id = fields[15]
    record = [fields[0], fields[7], fields[10][:5], fields[13], fields[14]]
    # Process only individual contributions and valid records
    if other_id.strip() == "" and valid_record(record):
        return record

def process_data(source, destination):
    campaign_data = source.read()
    percentile = float(percentile_source.read())
    # Data Structures
    donor_list = {} # Key: donor_id | Value: transaction_yr
    donation_dict = defaultdict(list) # Key: recipient | Value: list of transactions

    for row in campaign_data.splitlines():
        record = ingest_record(row)
        if not record:
            continue
        recipient, donor, zip_code, transaction_dt, transaction_amt = record
        transaction_yr = int(transaction_dt[4:])
        transaction_amt = int(round(float(transaction_amt)))
        donor_id = "-".join([donor, zip_code])
        recipient_id = "-".join([recipient, zip_code, str(transaction_yr)])

        # New donor
        if donor_id not in donor_list:
            donor_list[donor_id] = transaction_yr
        # Repeat donor
        # update transaction_yr if current contribution has calendar year prior to previous contribution
        elif transaction_yr < donor_list[donor_id]:
            donor_list[donor_id] = transaction_yr
        # perform calculations if current contribution has calendar year ahead of the previous contribution
        elif transaction_yr > donor_list[donor_id]:
            # Accumulate contributions as a list in the dictionary
            donation_dict[recipient_id].append(transaction_amt)
            transaction_cnt = len(donation_dict[recipient_id])
            contribution = sum(donation_dict[recipient_id])
            running_percentile = compute_percentile(donation_dict[recipient_id], percentile)

            output = [recipient, zip_code, str(transaction_yr), str(running_percentile), str(contribution), str(transaction_cnt)]
            write_to_destination(output, destination, '|')

def clean_up():
    source.close()
    destination.close()
    percentile_source.close()

if __name__ == "__main__":
    try:
        source = open(sys.argv[1], "r")
        percentile_source = open(sys.argv[2], "r")
        destination = open(sys.argv[3], "w")
    except Exception as e:
        print(e)
        sys.exit(1)

    process_data(source, destination)
    clean_up()
