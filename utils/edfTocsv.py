import numpy as np
import mne
import os
from os import listdir
from os.path import isfile, join

#File that transforms all EDF files contained in a folder into CSV files. 
#Note: The last column of the EDF files has been deleted in the CSV.

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) #string to the current path
mypath = THIS_FOLDER+"/edf/" #string to the path of edf files
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.sort()
#print(onlyfiles)

for i in range(len(onlyfiles)):
    edfFile = mypath+onlyfiles[i] #string path to the file
    fileName = onlyfiles[i]
    fileName = onlyfiles[i].replace('.edf','')
    print("edfFile: ", edfFile)
    edf = mne.io.read_raw_edf(edfFile) #read edf file
    A = edf.get_data() #get the data
    A = A[:-1] #remove the last column
    header = 'AF3,F7,F3,FC5,T7,P7,O1,O2,P8,T8,FC6,F4,F8,AF4'
    csvName = fileName+'.csv'
    csvFile = os.path.join(THIS_FOLDER, csvName)
    np.savetxt(csvFile, A.T, delimiter=',', header=header)