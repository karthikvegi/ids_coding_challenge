import sys
from datetime import datetime

# Input/Output
try:
    source = open(sys.argv[1], "r")
    percentile = open(sys.argv[2], "r")
    destination = open(sys.argv[3], "w")
except Exception as e:
    print(e)
    sys.exit(1)

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

def ingest_record(row):
    fields = row.split("|")
    other_id = fields[15]
    # Process the record if not an individual contribution
    if not other_id.strip():
        recipient = fields[0]
        donor = fields[7]
        zip_code = fields[10][:5]
        transaction_dt = fields[13]
        transaction_yr = transaction_dt[4:]
        transaction_amt = fields[14]
        record = [recipient, donor, zip_code, transaction_yr, transaction_amt]
        # Validate record before ingestion
        if not empty_fields(record) and not malformed_field(zip_code, 5) and not invalid_date(transaction_dt, '%m%d%Y'):
            return record

def clean_up():
    source.close()
    destination.close()
    percentile.close()

process_data(source)
clean_up()
