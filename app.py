import movieSpider as spidy
import IMDB_scraper

BASEPATH = 'G:\\movies\\'
scrapy = IMDB_scraper.IMDBscraper()

#----------Initializing App------------
#load pickled file here
spidy.loadMetaData(BASEPATH)

#walk current directory
spidy.getMovies(BASEPATH)

#check what all is new
f=1
for base in spidy.fileNamesC.keys():
    if base not in spidy.metaData:
        f=0

        #testing
        print(spidy.fileNamesC[base])

        #fetch imdb data
        try:
            details = scrapy.movieDetails(spidy.fileNamesC[base]['cleaned'])
            #testing
            print('got details')
            #add it to meta-data
            spidy.metaData[base] = {'details': details, 'filedata': spidy.fileNamesC[base]}
        except:
            print('Error while fetching')
#saving if changes were made
if f == 0:
    spidy.saveMetaData(BASEPATH)

print(spidy.metaData)

#----------Utility functions here------
#sorting
#grouping
#show copies

#some gui here if using python based