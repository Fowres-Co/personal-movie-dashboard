import os
import re
import pickle

MEDIAEXTS = ['.mp4','.mkv','.avi']
METAFILE = 'metadata.vif'

#metadata format - {basename:{imdb scraped data, rootpath},.....}
metaData = {}

#filesE contains lists of files of currRoot path
#filenamec has cleaned name of media files
currRoot, filesE, fileNamesC = [], [], {}

def getMovies(walkPath):
    global currRoot, directories, filesE, fileNamesC
    for path, dirnames, filenames in os.walk(walkPath):
        currRoot.append(path)
        #directories.append(dirnames) #not needed
        #seperating base and extension and storing as a tuple
        temp = []
        for name in filenames:
            base,ext =  os.path.splitext(name)
            temp.append((base,ext))
            #checking if media file. need to check for video lenght
            if ext in MEDIAEXTS:
                fileNamesC.setdefault(base, {})
                fileNamesC[base]['cleaned'], fileNamesC[base]['yr'] = nameCleaner(base) #returns name and year (1800 if not there)
                fileNamesC[base]['root'] = path
                fileNamesC[base]['ext'] = ext
        filesE.append(temp)

#cleaning the filename
def nameCleaner(base):
    mov = re.search(r'.*[0-9]{4}|.*',' '.join(re.findall(r'[A-Za-z]+|19[0-9]{2}|20[0-9]{2}|(?<![0-9])[0-9]{1,2}(?![0-9])', base)))
    name = ""
    yr = '1800'
    if mov:
        name = mov.group()
    if name:
        yre = re.search(r'[0-9]{4}', name) #assuming there is only 1 year in the string
        if yre:
            yr = yre.group()
            name = name[:yre.span()[0]] + name[yre.span()[1]:].rstrip()
            #testing
            print(yre.group(), name)
    return name, yr

#function to pickle and load pickled meta data
def loadMetaData(path):
    global metaData
    if metaData:
        print("Metadata already loaded.")
    else:
        try:
            with open(path+METAFILE,'rb') as fin:
                metaData = pickle.load(fin)
            fin.close()
        except (OSError, IOError) as e:
            print('Error while opening file')

def saveMetaData(path):
    global metaData
    if metaData:
        with open(path+METAFILE, 'wb') as fout:
            pickle.dump(metaData, fout, protocol=pickle.HIGHEST_PROTOCOL)
        fout.close()
    else:
        print('cant write nothing to file')