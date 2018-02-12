# Insight Data Engineering Coding Challenge
1. [Summary](README.md#summary)
2. [Inputs](README.md#inputs)
3. [Output](README.md#output)
4. [Considerations](README.md#considerations)
5. [Data Pipeline] (README.md#data-pipeline)
6. [Unit Test Cases] (README.md#unit-test-cases)

# Summary

The challenge involves working with the individual campaign contributions file from Federal Election Commission [FEC Website](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). The task is to identify repeat donors and compute a few values and write the results to an output file.

# Inputs

Two input files. 

1. `percentile.txt`, holds a single value -- the percentile value (1-100) that your program will be asked to calculate.

2. `itcont.txt`, has a line for each campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. 

From the campaign contribution file, we are only interested in the below fields:

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `NAME`: name of the donor
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

#### Data dictionary for the campaign contribution file [as described by the FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

## Output

The output file needs to be in the following format:

recipient | zip_code | transaction_year | running_percentile | contribution | transaction_cnt

    C00384516|02895|2018|333|333|1  

* `running_percentile`: computed using the **nearest-rank method** [as described by Wikipedia](https://en.wikipedia.org/wiki/Percentile).
* `contribution`: total contribution for the recipient in the zip_code and the year
* `transaction_cnt`: total number of transactions for the recipient in the zip_code and the year

## Considerations

1. A donor can be uniquely identified using the name and the zipcode is a repeat donor if he contributed in the prior calendar year
2. Each record should be treated as a sequentially streaming record with no chronological order 
3. Consider only first 5 digits of zipcode
4. Skip records with OTHER_ID field not empty (individual contributions only)
5. Skip processing record if:

* If `TRANSACTION_DT` is an invalid date (e.g., empty, malformed)
* If `ZIP_CODE` is an invalid zip code (i.e., empty, fewer than five digits)
* If the `NAME` is an invalid name (e.g., empty, malformed)
* If any lines in the input file contains empty cells in the `CMTE_ID` or `TRANSACTION_AMT` fields

## Data Pipeline

## Unit Test Cases
