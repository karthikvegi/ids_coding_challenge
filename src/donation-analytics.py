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

def write_to_destination(record, destination, delimiter):
    destination.write(delimiter.join(record) + "\n")

def ingest_record(row):
    record = {}
    fields = row.split("|")
    other_id = fields[15]
    # Process if not an individual contribution
    if not other_id.strip():
        return [fields[0], fields[7], fields[10][:5], fields[13], fields[14]]

def process_data(source):
    campaign_data = source.read()
    # var_list = ["recipient", "donor", "zip_code", "transaction_dt", "transaction_amt"]
    unique_donors = {}
    transactions = {}
    contributions = {}

    for row in campaign_data.splitlines():
        record = ingest_record(row)
        if record:
            recipient, donor, zip_code, transaction_dt, transaction_amt = record
            transaction_yr = int(transaction_dt[4:])

            if not empty_fields(record) and not malformed_field(zip_code, 5) and not invalid_date(transaction_dt, '%m%d%Y'):
                donor_id = donor + zip_code
                # Identify unique donor
                if donor_id not in unique_donors:
                    unique_donors[donor_id] = transaction_yr
                    continue
                # Identify repeat donor
                if donor_id in unique_donors and unique_donors[donor_id] < transaction_yr:
                    if recipient not in transactions:
                        transactions[recipient] = 1
                        contributions[recipient] = int(transaction_amt)
                    else:
                        transactions[recipient] += 1
                        contributions[recipient] += int(transaction_amt)
                    output = [recipient, zip_code, str(transaction_yr), str(contributions[recipient]), str(transactions[recipient])]
                    write_to_destination(output, destination, '|')

def clean_up():
    source.close()
    destination.close()
    percentile.close()

process_data(source)
clean_up()
