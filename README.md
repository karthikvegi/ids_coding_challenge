# Insight Data Engineering Coding Challenge
1. [Introduction](README.md#introduction)
2. [Challenge summary](README.md#challenge-summary)
3. [Details of challenge](README.md#details-of-challenge)
4. [Input files](README.md#input-files)
5. [Output file](README.md#output-file)
6. [Percentile computation](README.md#percentile-computation)
7. [Example](README.md#example)
8. [Writing clean, scalable and well-tested code](README.md#writing-clean-scalable-and-well-tested-code)
9. [Repo directory structure](README.md#repo-directory-structure)
10. [Testing your directory structure and output format](README.md#testing-your-directory-structure-and-output-format)
11. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
12. [FAQ](README.md#faq)

# Introduction
You’re a data engineer working for political consultants whose clients are cash-strapped political candidates. They've asked for help analyzing loyalty trends in campaign contributions, namely identifying areas of repeat donors and calculating how much they're spending.

The Federal Election Commission regularly publishes campaign contributions, and while you don’t want to pull specific donors from those files — because using that information for fundraising or commercial purposes is illegal — you want to identify areas (zip codes) that could be sources of repeat campaign contributions. 

# Challenge summary

For this challenge, we're asking you to take a file listing individual campaign contributions for multiple years, determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, `repeat_donors.txt`.

For each recipient, zip code and calendar year, calculate these three values for contributions coming from repeat donors:

* total dollars received
* total number of contributions received 
* donation amount in a given percentile

The political consultants, who are primarily interested in donors who have contributed in multiple years, are concerned about possible outliers in the data. So they have asked that your program allow for a variable percentile. That way the program could calculate the median (or the 50th percentile) in one run and the 99th percentile in another.

Another developer has been placed in charge of building the graphical user
interface with a dashboard showing the latest metrics on repeat donors, among other things. 

Your role on the project is to work on the data pipeline that will hand off the information to the front-end. As the backend data engineer, you do **not** need to display the data or work on the dashboard but you do need to provide the information.

You can assume there is another process that takes what is written to the output file and sends it to the front-end. If we were building this pipeline in real life, we’d probably have another mechanism to send the output to the GUI rather than writing to a file. However, for the purposes of grading this challenge, we just want you to write the output to files.

# Details of challenge

You’re given two input files. 

1. `percentile.txt`, holds a single value -- the percentile value (1-100) that your program will be asked to calculate.

2. `itcont.txt`, has a line for each campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. 

Out of the many fields listed on the pipe-delimited lines of `itcont.txt` file, you’re primarily interested in the contributor's name, zip code associated with the donor, amount contributed, date of the transaction and ID of the recipient. 

#### Identifying repeat donors
For the purposes of this challenge, if a donor had previously contributed to any recipient listed in the `itcont.txt` file in any prior calendar year, that donor is considered a repeat donor. Also, for the purposes of this challenge, you can assume two contributions are from the same donor if the names and zip codes are identical.

#### Calculations
Each line of `itcont.txt` should be treated as a record. Your code should process each line as if that record was sequentially streaming into your program.  In other words, your program processes every line of `itcont.txt` in the same order as it is listed in the file.

For each record that you identify as coming from a donor who has contributed to a campaign in a prior calendar year, calculate the running percentile of contributions from repeat donors, total number of transactions from repeat donors and total amount of donations streaming in from repeat donors so far for that calendar year, recipient and zip code. 

Write the calculated fields out onto a pipe-delimited line and then print it to an output file named `repeat_donors.txt` in the same order as the donation appeared in the input file.

## Input files

The Federal Election Commission provides data files stretching back years and is [regularly updated](http://classic.fec.gov/finance/disclosure/ftpdet.shtml).

For the purposes of this challenge, we’re interested in individual contributions. While you're welcome to run your program using the data files found at the FEC's website, you should not assume that we'll be testing your program on any of those data files or that the lines will be in the same order as what can be found in those files. Our test data files, however, will conform to the data dictionary [as described by the FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

Also, while there are many fields in the file that may be interesting, below are the ones that you’ll need to complete this challenge:

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `NAME`: name of the donor
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

### Input file considerations

Here are some considerations to keep in mind:

1. While the data dictionary has the `ZIP_CODE` occupying nine characters, for the purposes of the challenge, we only consider the first five characters of the field as the zip code
2. Because the data set doesn't contain a unique donor id, you should use the combination of `NAME` and `ZIP_CODE` (again, first five digits) to identify a unique donor
3. For the purposes of this challenge, you can assume the input file follows the data dictionary noted by the FEC for the 2015-current election years, although you should not assume the year field holds any particular value
4. The transactions noted in the input file are not in any particular order, and in fact, can be out of order chronologically
5. Because we are only interested in individual contributions, we only want records that have the field, `OTHER_ID`, set to empty. If the `OTHER_ID` field contains any other value, you should completely ignore and skip the entire record 
6. Other situations you can completely ignore and skip an entire record:

* If `TRANSACTION_DT` is an invalid date (e.g., empty, malformed)
* If `ZIP_CODE` is an invalid zip code (i.e., empty, fewer than five digits)
* If the `NAME` is an invalid name (e.g., empty, malformed)
* If any lines in the input file contains empty cells in the `CMTE_ID` or `TRANSACTION_AMT` fields

 Except for the considerations noted above with respect to `CMTE_ID`, `NAME`, `ZIP_CODE`, `TRANSACTION_DT`, `TRANSACTION_AMT`, `OTHER_ID`, data in any of the other fields (whether the data is valid, malformed, or empty) should not affect your processing. That is, as long as the previously noted considerations apply, you should process the record as if it was a valid, newly arriving transaction. (For instance, campaigns sometimes retransmit transactions as amendments, however, for the purposes of this challenge, you can ignore that distinction and treat all of the lines as if they were new)


## Output file

For the  output file that your program will create, `repeat_donors.txt`, the fields on each line should be separated by a `|`

The output should contain the same number of lines or records as the input data file, `itcont.txt`,  minus any records that were ignored as a result of the 'Input file considerations' and any records you determine did not originate from a repeat donor. 

Each line of this file should contain these fields:

* recipient of the contribution (or `CMTE_ID` from the input file)
* 5-digit zip code of the contributor (or the first five characters of the `ZIP_CODE` field from the input file)
* 4-digit year of the contribution
* running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar) 
* total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
* total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors

## Percentile computation

The first line of `percentile.txt` contains the percentile you should compute for these given input pair. For the percentile computation use the **nearest-rank method** [as described by Wikipedia](https://en.wikipedia.org/wiki/Percentile).

