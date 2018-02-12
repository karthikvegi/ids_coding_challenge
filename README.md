# Insight Data Engineering Coding Challenge
1. [Summary](README.md#challenge-summary)
3. [Details of challenge](README.md#details-of-challenge)
4. [Input files](README.md#input-files)
5. [Output file](README.md#output-file)
6. [Percentile computation](README.md#percentile-computation)


# Summary

The challenge involves working with the individual campaign contributions file from Federal Election Commission [FEC Website](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). The task is to identify repeat donors and compute a few values and write the results to an output file.

For each recipient, zip code and calendar year, calculate these three values for contributions coming from repeat donors:

* total dollars received
* total number of contributions received 
* donation amount in a given percentile

The political consultants, who are primarily interested in donors who have contributed in multiple years, are concerned about possible outliers in the data. So they have asked that your program allow for a variable percentile. That way the program could calculate the median (or the 50th percentile) in one run and the 99th percentile in another.

Another developer has been placed in charge of building the graphical user
interface with a dashboard showing the latest metrics on repeat donors, among other things. 

Your role on the project is to work on the data pipeline that will hand off the information to the front-end. As the backend data engineer, you do **not** need to display the data or work on the dashboard but you do need to provide the information.

You can assume there is another process that takes what is written to the output file and sends it to the front-end. If we were building this pipeline in real life, we’d probably have another mechanism to send the output to the GUI rather than writing to a file. However, for the purposes of grading this challenge, we just want you to write the output to files.

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

## Output File

The output file needs to be in the following format:

recipient | zip_code | transaction_year | running_percentile | contribution | transaction_cnt

    C00384516|02895|2018|333|333|1  

* `running_percentile`: computed using the **nearest-rank method** [as described by Wikipedia](https://en.wikipedia.org/wiki/Percentile).
* `contribution`: total contribution for the recipient in the zip_code and the year
* `transaction_cnt`: total number of transactions for the recipient in the zip_code and the year


