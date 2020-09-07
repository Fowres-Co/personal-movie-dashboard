import movieSpider as spidy
import IMDB_scraper
import os

#--- GUI
import eel

#--- testing custom logger
from xlogger import Logger

xLogger = Logger(__name__, 'info')
logger = xLogger.log #getting logging object
#---

BASEPATH = 'C:\\movietest\\'
MEDIAEXTS = ['.mp4','.mkv','.avi']
METAFILE = 'metadata.vif'

scrapy = IMDB_scraper.IMDBscraper()
logger.info("Initialized scraper")

#metadata format - {title1: {'name':'', other things from details..,'filedata':{file info here}}, title2: ..}
metaData = {}
loadedBaseNames = []
updateMetaFile = False
totalCount, fetchCount = 0, 0

#----------Initializing App------------
#load pickled file here
if metaData:
    logger.info("Metadata already loaded.")
else:
    metaData = spidy.loadMetaData(BASEPATH+METAFILE)
    loadedBaseNames = [val['filedata']['base'] for val in list(metaData.values())]
    logger.info('Loading metadata finished' + str(metaData))

#walk current directory
mediaFiles = spidy.getMediaFiles(BASEPATH, MEDIAEXTS)
logger.info('Walk completed')

#check what all is new
for file in mediaFiles:
    if file['base'] not in loadedBaseNames:
        totalCount += 1
        updateMetaFile = True
        
        #cleaning base name for  search
        cleanedName, year = spidy.nameCleaner(file['base'])
        logger.info('Found new - ' + str(cleanedName))
        
        #trying to fetch details
        try:
            logger.debug('Fetching: '+str(cleanedName)+' year:'+str(year))
            title, details = scrapy.movieDetails(cleanedName + ' ' + year)
            logger.info('Fetched details')
            fetchCount += 1
            
            #creating symbolic/soft link
            try:
                if not os.path.exists('web/symbs/videos'):
                    os.makedirs('web/symbs/videos')
                src = file['root'] + ('\\' if file['root'][-1] != '\\' else '') + file['base'] + file['ext']
                os.symlink(src, 'web/symbs/videos/'+title)
                metaData[title] = {'symlink':{'folder':'web/symbs/videos/', 'file':title}}
                logger.info(metaData[title]['symlink'])
            except FileExistsError:
                metaData[title] = {'symlink':{'folder':'web/symbs/videos/', 'file':title}}
            except:
                metaData[title] = {'symlink':''}
                logger.exception("I don't have the power to make symlinks :'(")

            #adding fetched details
            metaData[title]['filedata'] = file
            for key in details.keys():
                metaData[title][key] = details[key]
            logger.info('Added to metadata')

        except Exception as e:
            logger.exception('Error while fetching' + file['base'])

#saving if changes were made
if updateMetaFile:
    logger.info('Fetch Accuracy: ' + str(fetchCount/totalCount))
    spidy.saveMetaData(BASEPATH+METAFILE, metaData)
    logger.info('Saving Finished')
    updateMetaFile = False
else:
    logger.info('No new file')

#testing
# if len(metaData.keys()) > 0:
#     logger.debug(str(metaData[list(metaData.keys())[0]]))

#----------Utility functions here------
#sorting
#grouping
#show copies

#some gui here if using python based

eel.init('web')

@eel.expose
def getMovies():
    logger.debug('python in')
    ret = []
    for i in metaData:
        logger.debug(i+': '+metaData[i]['Name'])
        tl = {}
        tl['Poster'] = metaData[i]['Poster']
        tl['Name'] = metaData[i]['Name']
        tl['Summary'] = metaData[i]['Summary']
        tl['Symlink'] = metaData[i]['symlink']['file']
        ret.append(tl)
    logger.debug('python out')
    return ret

@eel.expose
def closeApp():
    eel.sys.exit(0)

startMode = {
    'dev': [],
    'dist': ['-start-fullscreen', '-kiosk']
}

#bloack and enter loop
try:
    eel.start('reactive.html', cmdline_args=startMode['dev'])
except SystemExit:
    pass
except:
    logger.exception('Eel start error')
