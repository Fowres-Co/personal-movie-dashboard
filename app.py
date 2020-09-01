import movieSpider as spidy
import IMDB_scraper

#--- GUI
import eel

#--- testing custom logger
from xlogger import Logger

xLogger = Logger(__name__, 'info')
logger = xLogger.log #getting logging object
#---

BASEPATH = 'C:\\movietest\\'
scrapy = IMDB_scraper.IMDBscraper()
logger.info("Initialized scraper")
updateMetaFile = False
totalCount, fetchCount = 0, 0

#----------Initializing App------------
#load pickled file here
spidy.loadMetaData(BASEPATH)
logger.info('Loading metadata finished')

#walk current directory
spidy.getMovies(BASEPATH)
logger.info('Walk completed')

#check what all is new
for base in spidy.fileNamesC.keys():
    if base not in spidy.metaData:
        totalCount += 1
        logger.info('Found new - ' + str(spidy.fileNamesC[base]))
        updateMetaFile = True
        try:
            logger.debug('Fetching: '+str(spidy.fileNamesC[base]['cleaned'])+' year:'+str(spidy.fileNamesC[base]['yr']))
            details = scrapy.movieDetails(spidy.fileNamesC[base]['cleaned'] + ' ' + spidy.fileNamesC[base]['yr'])
            logger.info('Fetched details')
            fetchCount += 1
            spidy.metaData[base] = {'details': details, 'filedata': spidy.fileNamesC[base]}
            logger.info('Added to metadata')
        except Exception as e:
            logger.exception('Error while fetching:')

#saving if changes were made
if updateMetaFile:
    logger.info('Fetch Accuracy: ' + str(fetchCount/totalCount))
    spidy.saveMetaData(BASEPATH)
    logger.info('Saving Finished')
    updateMetaFile = False
else:
    logger.info('No new file')

#testing
# for i in range(5):
#     if len(spidy.metaData.keys()) >= 5:
#         logger.debug(str(spidy.metaData[list(spidy.metaData.keys())[i]]))

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
    for i in spidy.metaData:
        tl = {}
        tl['Poster'] = spidy.metaData[i]['details'][1]['Poster']
        tl['Name'] = spidy.metaData[i]['details'][1]['Name']
        tl['Summary'] = spidy.metaData[i]['details'][1]['Summary']
        ret.append(tl)
    logger.debug('python out')
    return ret

@eel.expose
def closeApp():
    eel.sys.exit(0)

#bloack and enter loop
eel.start('main.html', port=8080, cmdline_args=['--start-fullscreen', '--kiosk'])
