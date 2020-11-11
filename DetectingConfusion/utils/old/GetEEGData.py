#Following script aims to provide an easy way to get 14 recorded EEG channels for each exercice
#First it syncs Emotiv TestBench output with faceT output and screenrecording
#Then it uses the start and end time of each exercise to access the EEG data recorded at that time via TestBench. 
#(Start and end time of each exercice was found watching the screenrecording)
#Then it saves them in a csv file for each exercise (20 in total).

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

from datetime import datetime, timedelta

################ PARAMETERS TO CHANGE FOR EACH PARTICIPANT ####################################################################

# WARNING: This work only if eeg were recorded before iMotions

# At which frequence eeg data were recorded
eegSampling = 128

# timebase
eegStartingCounter = 93

# Date of recorded data
eegDate_ = '11:09:08'

#EEG csv file
csvName= './P1.csv'

#Time at which each exercise (20 in total) begins and its duration in seconds (based on exercices csv file)
exercicesTime = [['11:10:47.12',9,'s0ex0'],['11:11:11.22',38,'s0ex1'],['11:11:54.91',61,'s0ex2'],['11:13:01.84',50,'s0ex3'],\
    ['11:15:23.49',33,'s1ex0'],['11:16:05.56',136,'s1ex1'],['11:18:24.20',77,'s1ex2'],['11:19:47.34',141,'s1ex3'],\
    ['11:23:10.33',51,'s2ex0'],['11:24:07.86',52,'s2ex1'],['11:25:05.13',60,'s2ex2'],['11:26:08.75',282,'s2ex3'],\
    ['11:32:58.38',65,'s3ex0'],['11:34:06.81',35,'s3ex1'],['11:34:45.69',52,'s3ex2'], ['11:35:41.87',50,'s3ex3'],\
    ['11:36:46.75',21,'s4ex0'],['11:37:16.50',20,'s4ex1'],['11:38:01.49',21,'s4ex2'],['11:38:54.58',21,'s4ex3']]

##########################################################################################################


csvFile = os.path.join(THIS_FOLDER, csvName)

#
eegFreq = eegSampling

#OpenCSV, get data from the CSV
import csv
import sys
import numpy as np


#Get data from CSV
def GetData():
    # Read CSV file
    kwargs = {'newline': ''}
    mode = 'r'
    if sys.version_info < (3, 0):
        kwargs.pop('newline', None)
        mode = 'rb'
    with open(csvFile, mode, **kwargs) as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]
    return data_read[1:]

dataBase = GetData()
dataBase = np.array(dataBase, dtype=np.float) #numpy array is easier to manipulate
#print(dataBase)

# Get EEG starting time with seconds and 2 decimals
def GetEEGStartingTime():
    eegMilliseconds = int((eegStartingCounter/eegFreq)*100)
    if (int(eegMilliseconds/10)==0):
        decimals = '0'+str(eegMilliseconds)
    else:
        decimals = str(eegMilliseconds)
    print("EEG starting time in seconds with 2 decimals: "+eegDate_+'.'+decimals)
    return eegDate_+'.'+decimals

# Delay between start of eeg recording and start of the selected exercice with 2 decimals
def CalculateDelay(exerciceTime):
    # Date of created csv that contains 14 eeg signals
    eegDate = datetime.strptime(GetEEGStartingTime(), '%H:%M:%S.%f')
    # Date of start of the exercice
    exTime = datetime.strptime(exerciceTime, '%H:%M:%S.%f')

    # Delay between starting capture and next exercice (recorded in seconds with 2 decimals)
    delay = abs(eegDate-exTime)
    delay = delay.total_seconds()
    print('Delay between eeg start of recording and exercice: ',delay)
    return delay


# Calculate how many rows we need to pass to be synched with exercice
def CalculateNbRowsToNextExercice(exerciceTime):
    delRow1 = int(CalculateDelay(exerciceTime))*eegFreq
    
    delRow2 = CalculateDelay(exerciceTime)-int(CalculateDelay(exerciceTime))
    #delRow3 = float(str(delRow2)[:4])
    delRow3 = float('%.2f'% (delRow2))
    delRow4 = int(delRow3*eegFreq)

    print("delrow1, delrow2, delrow3",delRow1,delRow2,delRow3)
    global nbRowToDelete
    nbRowToDelete = delRow1+delRow4
    print("nbrowtodelete: ",nbRowToDelete)
    return nbRowToDelete


#Remove EEG Data and moving forward
def GoToNextEEGData(exerciceTime):
    db = np.delete(dataBase, np.s_[0:CalculateNbRowsToNextExercice(exerciceTime)],axis = 0)
    return db

#Store EEG 14channels raw signals of the exercice
def CreateArrayExercice(data,exDuration):
    lastRow = exDuration*eegFreq
    db = data[0:lastRow+1]
    #Extract raw signal only
    db = db[:, 2:16]
    return db

#Save EEG 14 channels raw signals into a CSV file
def SaveDataExercice(dataExercice,filename):
    filename = './'+filename+'.csv'
    csvExport = os.path.join(THIS_FOLDER, filename)
    np.savetxt(csvExport, dataExercice, delimiter=",", header = "AF3,F7,F3,FC5,T7,P7,O1,O2,P8,T8,FC6,F4,F8,AF4", fmt='%f')

#Explore EEG single dataset and move forward in time
def MovingForward(exerciceTime):
    data = GoToNextEEGData(exerciceTime)
    return data

#Create CSV 
def NextExercice(exDuration,filename,data):
    db = data
    dataExercice = CreateArrayExercice (db,exDuration)
    print('Before last row: End exercice',dataExercice[len(dataExercice)-2],'\n Last row: End exercice',dataExercice[len(dataExercice)-1])
    SaveDataExercice(dataExercice,filename)

#Create CSV for each exercices
def GenerateExercicesCSV():
    for i in range(len(exercicesTime)):
        data = MovingForward(exercicesTime[i][0])
        print('Row 1: Start exercice',data[0],'\n Row 2: Start exercice',data[1])
        filename = exercicesTime[i][2]
        NextExercice(exercicesTime[i][1],filename,data)

GenerateExercicesCSV()
#print(dataBase)