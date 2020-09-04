import os
import re
import pickle

#--- testing custom logger
from xlogger import Logger

xLogger = Logger(__name__, 'info')
logger = xLogger.log #getting logging object
#---

def getMediaFiles(walkPath, mExts):
    mediaFiles, baseNames = [], []

    for path, dirnames, filenames in os.walk(walkPath):
        for name in filenames:
            base,ext =  os.path.splitext(name) #seperating base and extension and storing as a tuple
            
            #checking if media file. need to check for video lenght
            if ext in mExts:
                mediaFiles.append({'root':path, 'base':base, 'ext': ext})
                baseNames.append(base)
                logger.info('found - ' + mediaFiles[-1]['base'])

    return mediaFiles

#cleaning the filename
#returns name and year (1800 if not there)
def nameCleaner(base):
    name = ""
    yr = '1800'

    mov = re.search(r'.*[0-9]{4}|.*',' '.join(re.findall(r'[A-Za-z]+|19[0-9]{2}|20[0-9]{2}|(?<![0-9])[0-9]{1,2}(?![0-9])', base)))
    if mov:
        name = mov.group()
    else:
        logger.error('No name found in base')

    if name:
        yre = re.search(r'[0-9]{4}', name) #assuming there is only 1 year in the string
        if yre:
            yr = yre.group()
            name = name[:yre.span()[0]] + name[yre.span()[1]:].rstrip()
            logger.info(yre.group() +' '+ name)
        else:
            logger.error('No year in cleaned name')

    return re.sub(r' +',' ',name.lstrip().rstrip()), yr

#function to pickle and load pickled meta data
def loadMetaData(path):
    try:
        with open(path,'rb') as fin:
            metaData = pickle.load(fin)
        fin.close()
        logger.info('Metadata loaded successfully')
        return metaData
    except (OSError, IOError) as e:
        logger.exception('Error while opening file')
        return {}

def saveMetaData(path, metaData):
    if metaData:
        with open(path, 'wb') as fout:
            pickle.dump(metaData, fout, protocol=pickle.HIGHEST_PROTOCOL)
        fout.close()
        logger.info('Metadata saved successfully.')
    else:
        logger.error('Cannot write empty metadata to file.')

#testing
# getMovies('c:\\movietest\\')