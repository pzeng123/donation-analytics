# Introduction
The Insight Data Engineering Coding Challenge problem could be found [here](https://github.com/InsightDataScience/donation-analytics).

This solution was developed with Python 3.6

Required python modules:
 * sys
 * time
 * datetime
 * math
 * numpy


# Input and Output
Input directory has `itcont.txt` and `percentile.txt` files. The `percentile.txt` contains a number (0~100) representing the percentile to be considered during processing. The `itcont.txt` follow the conventions set forth by the [FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

The donation analytics for repeat donors is `repeat_donors.txt` and it appears in the `output` directory.

# Method

The input file was read line by line and it will be skipped if it's invalid: 
1. `TRANSACTION_DT` is an invalid date
2. `ZIP_CODE` is an invalid zip code
3. `NAME` is an invalid name
4. `CMTE_ID` or `TRANSACTION_AMT` is empty
5. `OTHER_ID` is NOT empty  

While reading the input file, data were stored in these two dictionaries: `donor_dic` and `recipient_dic`.

`donor_dic` is `donor_dic{ZIP_CODE:{NAME:TRANSACTION_YEAR}}` that stores donor's Zipcode, Name, and the first donation year in the input file. For a new streaming in record, if the donor is in this dictionary and the year is large than the donor's dictionary year value, it's a repeated donor's donation, and the contribution number will go to the next step. 

`recipient_dic` is `recipient_dic{ZIP_CODE:{CMTE_ID:{TRANSACTION_YEAR:[contributions list]}` that stores a list of recipient's recieved contributioins based on the Zipcode, CMTE_ID and the year of contributions.

Then `numpy.percentile()` with `nearest` method was used to calculate the running percentile of the recieved contributioins for the Zipcode, CMTE_ID and the year of contributions.

At last, the results were write to the output file `repeat_donors.txt`.

# Run Instructions
To run the program, execute `./run.sh` at the root directory of the project.

# Tests Instructions
In the 'insight_testsuite' directory, 6 different tests were tested.
1. original insight_testsuite test
2. added some more donation records based on 1
3. changed `percentile` from 30 to 50
4. added some invalid records such as invalid zipcode, invalid date, invalid ID and so on.
5. the input file is a 17.6M file contains the first 100000 lines of Contributions by Individuals 2017 - 2018 Data File by [FEC](https://classic.fec.gov/finance/disclosure/ftpdet.shtml#a2017_2018).
6. a minimal input file 

To test the program using the testsuite, execute `./run_tests.sh` at the 'insight_testsuite' directory.

# Discussion

Maybe we need to discuss how to identify repeat donors?
In the project description, "For the purposes of this challenge, if a donor had previously contributed to any recipient listed in the itcont.txt file `in any prior calendar year`, that donor is considered a repeat donor". That means it won't count if repeat contributed in the same year, which could make people confused. For example, considering the situation that a person donated on 01012017, and donated on 02012017, it's not a repeat donation.



