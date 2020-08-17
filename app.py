import movieSpider as spidy
import IMDB_scraper

#--- testing custom logger
from xlogger import Logger

#loggger set to log debug and up where errors are logged to file 'error.log'
xLogger = Logger(__name__, 'debug', filelevel = 'error')
xLogger.makeFileHandler('info')
logger = xLogger.log #getting logging object
#---

BASEPATH = 'C:\\movietest\\'
scrapy = IMDB_scraper.IMDBscraper()
logger.info("Initialized scraper")

#----------Initializing App------------
#load pickled file here
spidy.loadMetaData(BASEPATH)
logger.info('Loading metadata finished')

#walk current directory
spidy.getMovies(BASEPATH)
logger.info('Walk completed')

#check what all is new
updateMetaFile = False
for base in spidy.fileNamesC.keys():
    if base not in spidy.metaData:
        logger.info('Found new - ' + str(spidy.fileNamesC[base]))
        updateMetaFile = True
        try:
            logger.debug('Fetching: '+str(spidy.fileNamesC[base]['cleaned'])+' year:'+str(spidy.fileNamesC[base]['yr']))
            details = scrapy.movieDetails(spidy.fileNamesC[base]['cleaned'] + ' ' + spidy.fileNamesC[base]['yr'])
            logger.info('Fetched details')
            spidy.metaData[base] = {'details': details, 'filedata': spidy.fileNamesC[base]}
            logger.info('Added to metadata')
        except Exception as e:
            logger.exception('Error while fetching:')

#saving if changes were made
if updateMetaFile:
    spidy.saveMetaData(BASEPATH)
    logger.info('Saving Finished')
    updateMetaFile = False
else:
    logger.info('No new file')

#testing
# xLogger.makeStreamHandler()
# for i in range(5):
#     if len(spidy.metaData.keys()) >= 5:
#         logger.debug(str(spidy.metaData[list(spidy.metaData.keys())[i]]))

#----------Utility functions here------
#sorting
#grouping
#show copies

#some gui here if using python based