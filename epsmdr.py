# Import os module
import os
import re
import sys
import getopt
import datetime
from builtins import int

'''
EPSMDR extractor version: 0.1.1 ALPHA
2019/11/04 07:32

'''
""" Read CSV SMDR file created  by Avaya IP Office 
    extracting lines with numbers, extensions or user names matching
     
TODO:update CSV header from SMDR file - done
TODO:Searching for records matching particular users or period
"""


extList = ["E7615","E7619","E7694","E7610","E7143","E7609","E7607", "E7617","E7604","E7614","E7185","E7626"]
CommandOptions = sys.argv
# getopt to get input options for import


def main(argv):
    # TODO: Separate function/smippet
    # Analize run options and extract file names or display help text: epsmdr.py -i <inputfile> -o <outputfile>
    inputfile = ''
    outputfile = ''
    
    # Get startup options using getopt
    try:
        opts, args = getopt.getopt(argv,"hi:o:d:D:",["ifile=","ofile=","date=","directory="])
    except getopt.GetoptError as err: # FIXME: not throwing error correctly - 
        print(err)
        print('Error use format epsmdr.py -i <inputfile> -o <outputfile> -d YYYY/MM/dd')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Error use format epsmdr.py -i <inputfile> -o <outputfile> -d YYYY/MM/dd')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            if arg != "" :
                inputfile = arg
            else: 
                inputfile = "folder" 
        elif opt in ("-o", "--ofile"):
            if arg != "":
                outputfile = arg
            else:
                outputfile="epsmdr.csv"
        elif opt in ("-d", "--startdate"):
            startdate = arg
        elif opt in ("-D", "--directory"):
            searchdirectory = arg
        else:
            None

    CSV_header = "Call Start,Connected Time,Ring Time,Caller,Direction,Called Number,Dialled Number,\
Account,Is Internal,Call ID,Continuation,Party1Device,Party1Name,Party2Device,Party2Name,\
Hold Time,Park Time,Auth Valid,Auth Code,User Charged,Call Charge,Currency,Account at Last User Change,\
Call Units,Units at Last User Change,Cost per Unit,Mark Up,External Targeting Cause,\
External Targeter Id,External Targeted Number"

    outputfile = open(outputfile, 'w')
    outputfile.write(CSV_header + "\n")
    
    line = CSV_header
     
    correct_date = True
    year, month, day = startdate.split("/")
    try :
        datetime.datetime(int(year),int(month),int(day))
    except ValueError:
        correct_date = False
        print("wrong date")
        sys.exit(2)

    # Check if date is valid - example week period: 2019/12/30 - 2020/01/05
    if correct_date:
        d = datetime.date(int(year),int(month),int(day))
        # today = datetime.date.today()
        seven_days = []
        for daycount in range(0,7) :
            seven_days.insert(daycount,str(d.strftime("%Y/%m/%d")))
            d=d+datetime.timedelta(days=1)
    line_complete = re.compile(r"^20[1-3][0-9]/[01][0-9]/[0-3][0-9]\s[012][0-9]:[0-5][0-9]:[0-5][0-9],"
                            r"\d{2}:\d{2}:\d{2}.*20[1-3][0-9]/[01][0-9]/[0-3][0-9]\s[012][0-9]:[0-5][0-9]:[0-5][0-9]$")
    for fname in os.listdir(searchdirectory):
        if re.match(r'[2][0][1-3][0-9]\.[01][0-9]\.csv',fname): # test if file extension CSV or TXT
            try:
                with open(searchdirectory+"\\"+fname, 'r') as fo:

                    while line != '':
                        line = fo.readline()
                        c = line_complete .match(line)
                        if c == None and line != '':        # Check if line complete
                            tmpline = fo.readline()         # If not gen next line from file
                            line = line.rstrip()+tmpline    # and join them together
                        # TODO: search for all elements in the list and if any will match copy line to output file
                        # TODO: start date as an option plus how many days - default 7
                        #
                        for lineDate in seven_days:
                            reDate = re.compile("^("+lineDate+").*$")
                            m = reDate.match(line)
                            # print(line)
                            if m is not None:
                                c = line_complete .match(line)
                                if c is not None :
                                    for ext in extList :
                                        index = line.find(ext)  # TODO: create search procedure for elements in the list
                                        if index != -1:
                                            outputfile.write(line)
                    fo.close()
                
                line = '\n'     
            except IOError:
                print(os.path.dirname(os.path.abspath(__file__)))
                print ("Could not read file: ", inputfile)
            
    outputfile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
# TODO: convert EP scripts into more generic Python Aplication to build simple reports from Avaya SMDR logs
# TODO: create listening service to receive SMDR directly then build reports