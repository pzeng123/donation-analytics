import sys
import time
import datetime
import numpy as np
import math


def isValid(item, category):
    '''
    check if the item in the category is valid.
    
    input strings
    returns True or False

    return False if:
    1. TRANSACTION_DT is an invalid date
    2. ZIP_CODE is an invalid zip code
    3. NAME is an invalid name
    4. CMTE_ID or TRANSACTION_AMT is empty
    5. OTHER_ID is NOT empty    
    '''
    # OTHER_ID should be empty for "individual contributions"
    if category == 'OTHER_ID':
        return item == ''
    
    # invalid CMTE_ID: not alphanumeric, lenth is not 9
    if category == 'CMTE_ID':
        if not item.isalnum() or len(item) != 9:
            return False
    
    # invalid TRANSACTION_AMT: empty, not a number, <0
    if category == 'TRANSACTION_AMT':
        if not item:
            return False
        try:
            float(item)
        except(ValueError, TypeError):
            return False
        if float(item) < 0:
            return False
        
    # invalid ZIP_CODE: not digit, lenth not in 5~9     
    if category == 'ZIP_CODE':
        if not item.isdigit() or len(item) < 5 or len(item) > 9:
            return False

    # invalid NAME: empty, malformed 
    if category == 'NAME':
        if not item or len(item) > 200:
            return False
       
    # invalid TRANSACTION_DT: empty, not digit, malformed 
    if category == 'TRANSACTION_DT':
        if not item.isdigit() or len(item) != 8:
            return False
        year, month, day = int(item[4:]), int(item[:2]), int(item[2:4])
        try:
            newDate = datetime.datetime(year, month, day)
        except ValueError:
            return False
    return True

def main():
    input_path = './input/itcont.txt'
    PERCENTILE_path = './input/percentile.txt'
    output_path = './output/repeat_donors.txt'
    
    if len(sys.argv) == 4:
        input_path = sys.argv[1]
        PERCENTILE_path = sys.argv[2]
        output_path = sys.argv[3]
    else:
        print(" Path Error" )
        return

    # Read the 'percentile.txt' file to get the PERCENTILE number
    with open(PERCENTILE_path, "r") as PERCENTILE_file:
        PERCENTILE = PERCENTILE_file.readline().rstrip()
        if not PERCENTILE.isdigit() or int(PERCENTILE) < 0 or int(PERCENTILE) > 100:
            print(" Percentile Error" )
            return    

    # data structure: data stored in 2 dictionaries: donor_dic and recipient_dic
    # donor_dic{ZIP_CODE:{NAME:TRANSACTION_YEAR}}
    # recipient_dic{ZIP_CODE:{CMTE_ID:{TRANSACTION_YEAR:[contributions list]}
    
    donor_dic = {}
    recipient_dic = {}
    total_num, valid_num, repeat_donation_num = 0, 0, 0

    with open(input_path, "r") as inputfile:
        with open(output_path, "w") as outputfile:
            for current_line in inputfile:
                if current_line == '\n':
                    continue
                total_num += 1

                # Split the line to get the information each filed which is divided by '|'
                line_list = current_line.split('|')
                
                CMTE_ID = line_list[0]
                NAME = line_list[7]
                ZIP_CODE = line_list[10]
                TRANSACTION_DT = line_list[13]
                TRANSACTION_AMT = int(line_list[14])
                OTHER_ID = line_list[15]
                
                # Completely ignore and skip an entire record if this record is not valid:
                if not isValid(TRANSACTION_DT, 'TRANSACTION_DT') or not isValid(ZIP_CODE, 'ZIP_CODE') or not isValid(NAME, 'NAME') or not isValid(CMTE_ID, 'CMTE_ID') or not isValid(TRANSACTION_AMT, 'TRANSACTION_AMT') or not isValid(OTHER_ID, 'OTHER_ID'):
                    continue
                
                valid_num += 1
                ZIP_CODE = line_list[10][:5]
                TRANSACTION_YEAR = int(TRANSACTION_DT[4:])
                
                # Check if current donor is a repeat donor (donors information stored in donor_dic) 
                # here the current TRANSACTION_YEAR of a repeat donor must larger than the stored donor value
                # for example, TRANSACTION_YEAR stored for donor 'A' is 2017, then other 2017 transactions for donor 'A' will be skipped
                if not ZIP_CODE in donor_dic:
                    donor_dic[ZIP_CODE] = {NAME:TRANSACTION_YEAR}
                    continue
                elif not NAME in donor_dic[ZIP_CODE]:
                    donor_dic[ZIP_CODE][NAME] = TRANSACTION_YEAR
                    continue
                elif donor_dic[ZIP_CODE][NAME] >= TRANSACTION_YEAR:
                    continue
                
                repeat_donation_num += 1
                # for repeat donor, this contribution added to recipient_dic[ZIP_CODE][CMTE_ID][TRANSACTION_YEAR]
                if not ZIP_CODE in recipient_dic:
                    recipient_dic[ZIP_CODE] = {CMTE_ID:{TRANSACTION_YEAR:[TRANSACTION_AMT]}}
                elif not CMTE_ID in recipient_dic[ZIP_CODE]:
                    recipient_dic[ZIP_CODE][CMTE_ID] = {TRANSACTION_YEAR:[TRANSACTION_AMT]}
                elif not TRANSACTION_YEAR in recipient_dic[ZIP_CODE][CMTE_ID]:
                    recipient_dic[ZIP_CODE][CMTE_ID][TRANSACTION_YEAR] = [TRANSACTION_AMT]
                else:
                    recipient_dic[ZIP_CODE][CMTE_ID][TRANSACTION_YEAR].append(TRANSACTION_AMT)
                       
                # Calculate the running percentile, using numpy.percentile() with 'nearest' method
                running_contributions = recipient_dic[ZIP_CODE][CMTE_ID][TRANSACTION_YEAR]
                running_percentile = np.percentile(running_contributions, PERCENTILE, interpolation='nearest')
                if running_percentile - math.floor(running_percentile) < 0.50:
                    running_percentile = math.floor(running_percentile)
                else:
                    running_percentile = math.ceil(running_percentile)

                # Write to output file. Example: "C00384516|02895|2018|333|333|1"
                outputfile.write(CMTE_ID + '|' + ZIP_CODE + '|' + str(TRANSACTION_YEAR) + '|' + str(running_percentile) + '|' + str(sum(running_contributions)) + '|' + str(len(running_contributions)) + '\n')
                
    print("Complete")
    print("{} valid records in {} total records, and {} invalid records skipped.".format(valid_num, total_num, total_num - valid_num))
    print("Repeated donation records written into output file: {}".format(repeat_donation_num)) 

print("Running...")    
start_time = time.time()
main()
print("Total processing time: {} seconds".format(round(time.time() - start_time)))    
               
            

