import os
import re
import pickle

MEDIAEXTS = ['.mp4','.mkv','.avi']
METAFILE = 'metadata.vif'

#metadata format - {id:{imdb scraped data},.....} id:could be a number
#id lookup: {"base name": id}
metaData = {}
idLookup = {}

#dirs, filesE and fileNamesC contains respective lists of currRoot path
currRoot, directories, filesE, fileNamesC = [], [], [], []

#poor formating
def getMovies(walkPath):
    global currRoot, directories, filesE, fileNamesC
    for path, dirnames, filenames in os.walk(walkPath):
        currRoot.append(path)
        directories.append(dirnames)
        #seperating base and extension and storing as a tuple
        temp = []
        for name in filenames: 
            temp.append(os.path.splitext(name))
        filesE.append(temp)

    #function would be better?
    for flist in filesE:
        temp = []
        for base,ext in flist:
            if ext in MEDIAEXTS:
                #cleaning the filename
                mov = re.match(r'.*[0-9]{4}|.*',' '.join(re.findall(r'[A-Za-z]+|19[0-9]{2}|20[0-9]{2}|(?<![0-9])[0-9]{1,2}(?![0-9])', base)))
                name = ""
                if mov:
                    name = mov.group()
                #print(name,":",base)
                temp.append(name)
        fileNamesC.append(temp)
    #maybe no need to return just call the function and use the stored values
    #return currRoot, directories, filesE, fileNamesC

#function to pickle and load pickled meta data
def loadMetaData():
    if metaData:
        print("Metadata already loaded.")
    else:
        with open(METAFILE,'rb') as fin:
            metaData = pickle.load(fin)
        fin.close()

def saveMetaData():
    if metaData:
        with open(METAFILE, 'wb') as fout:
            pickle.dump(metaData, fout, protocol=pickle.HIGHEST_PROTOCOL)
        fout.close()
    else:
        print('cant write nothing to file')