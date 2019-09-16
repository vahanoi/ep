# Import os module
import os
import re
from typing import List, Any, Union
from test.sortperf import flush

'''
QOS string example

2019-09-05T12:41:17 3042740332mS PRN: QOS Data: Call ID=62698 Device=Phone(Number=7605, BaseExtn=7605) IP Address:192.168.222.96 Peer IP Address:192.168.251.2 Call Duration=29s
2019-09-05T12:41:17 3042740332mS PRN: QOS Data Continued Jitter: Max=0ms Avg=0ms Round Trip Delay: Max=16ms Avg=15ms Packet Loss: Max=0/1000 Avg=0/1000

1. join string into single line
2. use regular expression to check error values
3. extract details to a CSV (?) for Excel analysis

'''

# Ask the user to enter string to search
search_path = input("Enter directory path to search : ")
file_type = input("File Type : ")
# search_str = input("Enter the search string : ") # Enter search string - disabled for default QOS Data string
search_str_line1 = "PRN: QOS Data"

# https://regex101.com/r/LZCAu4/2
regex_line1 = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}).(\d*)[a-zA-Z :=]{26}(\d*)[Da-z= ]{8}([a-zA-Z]*)"
                         r"[a-zA-Z(=]{8}(\d*)[a-zA-Z=, ]{11}(\d*)\) [a-zA-Z: ]{11}(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
                         r"[a-zA-Z :]{17}(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[a-zA-Z =]{15}(\d*)s$")

# CSV_values: = [['cDate', ''], [cTime, '']]

search_str_line2 = "PRN: QOS Data Continued"

# https://regex101.com/r/7aaBZ1/1
regex_line2 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d*[a-zA-Z :=]{39}(\d*)ms.Avg=(\d*)ms[a-zA-Z :=]*"
                         r"(\d*)ms Avg=(\d*)[a-zA-Z:= ]*(\d*\/\d*) Avg=(\d*\/\d*)$")


CSV_header = "Date,Time,ms,Call ID,Device Type,Number,BaseExtn,IP Address,Peer IP Address,Call Duration,Jitter Max," \
                "Jitter Avg,Round Trip Delay Max,Round Trip Avg, Packet Loss Max, Packet Loss Avg"
output_file = input("Enter output file name : ")
outputfile = open(output_file,'w')
outputfile.write(CSV_header + "\n") # Write CSV header with new line at the end
line_found = False  # Initialise line_found as False
joined_line = ""

# Append a directory separator if not already present
if not (search_path.endswith("/") or search_path.endswith("\\") ): 
        search_path = search_path + "/"

# If path does not exist, set search path to current directory
if not os.path.exists(search_path):
        search_path = "."

# Repeat for each file in the directory  
for fname in os.listdir(path=search_path):
    #  outputfile.write("\n\n"+fname+"\n\n")
    # Apply file type filter   
    if fname.endswith(file_type):

        # Open file for reading
        fo = open(search_path + fname)

        # Read the first line from the file
        line = fo.readline()

        # Initialize counter for line number
        line_no = 1
        csv_line = ''
        block_list = []
        # Loop until EOF
        while line != '':
                # Search for first QOS line
                index = line.find(search_str_line1)
                # print("line: ", line_no)
                if index != -1 and line_found == False :
                    line_found = True  # if first match found
                    line1_list = regex_line1.split(line) # Split first line using RegEx rules to extract values

                    # print (line1_list)
                    joined_line = line

                # Read next line

                if line_found:
                    line = fo.readline()
                    line2_list = regex_line2.split(line)
                    line_list = line1_list + line2_list
                    line_found = False
                    for element in line_list:  # Write lists to file in CSV format
                        if element != '' and element != '\n':
                            csv_line = csv_line + element + ','  # Formatting CSV line

                if csv_line != '':
                    csv_line = csv_line + '\n'  # Add next line symbol at the end of CSV line
                    outputfile.write(csv_line)  # Write line to a file
                    # print (csv_line)
                    csv_line = ''  # Empty CSV line after adding to a file
                # Read  new line from current file
                line = fo.readline()  

                # Increment line counter
                line_no += 1
                if line_no % 1000 == 0:  # if modulo = 0 print line number (every 1000) 
                    print ("\rProcessed:", line_no, "lines",end="", flush=True)

        # Close the files
        fo.close()
outputfile.close()