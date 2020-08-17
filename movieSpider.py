import os
import re
import pickle

#--- testing custom logger
from xlogger import Logger

#loggger set to log debug and up where errors are logged to file 'error.log'
xLogger = Logger(__name__, 'debug', filelevel = 'error')
xLogger.makeFileHandler('info')
logger = xLogger.log #getting logging object
#---

MEDIAEXTS = ['.mp4','.mkv','.avi']
METAFILE = 'metadata.vif'

#metadata format - {basename:{imdb scraped data, rootpath....},.....}
metaData = {}

#filesE contains lists of files of currRoot path
#filenamec has cleaned name of media files
currRoot, filesE, fileNamesC = [], [], {}

def getMovies(walkPath):
    global currRoot, filesE, fileNamesC

    for path, dirnames, filenames in os.walk(walkPath):
        currRoot.append(path)
        
        temp = []
        for name in filenames:
            base,ext =  os.path.splitext(name) #seperating base and extension and storing as a tuple
            temp.append((base,ext))
            
            #checking if media file. need to check for video lenght
            if ext in MEDIAEXTS:
                fileNamesC.setdefault(base, {})
                fileNamesC[base]['cleaned'], fileNamesC[base]['yr'] = nameCleaner(base)
                fileNamesC[base]['root'] = path
                fileNamesC[base]['ext'] = ext
                logger.info('found - ' + str(fileNamesC[base]))
        
        filesE.append(temp)

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
    global metaData

    if metaData:
        logger.info("Metadata already loaded.")
    else:
        try:
            with open(path+METAFILE,'rb') as fin:
                metaData = pickle.load(fin)
            fin.close()
            logger.info('Metadata loaded successfully')
        except (OSError, IOError) as e:
            logger.exception('Error while opening file')

def saveMetaData(path):
    global metaData

    if metaData:
        with open(path+METAFILE, 'wb') as fout:
            pickle.dump(metaData, fout, protocol=pickle.HIGHEST_PROTOCOL)
        fout.close()
        logger.info('Metadata saved successfully.')
    else:
        logger.error('Cannot write empty metadata to file.')

#testing
# xLogger.makeStreamHandler() #logging debugs and up to console for testing
# getMovies('c:\\movietest\\')