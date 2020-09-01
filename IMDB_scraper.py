from bs4 import BeautifulSoup
import requests
from shutil import copyfileobj
<<<<<<< Updated upstream

from os import path, makedirs
=======
>>>>>>> Stashed changes

#--- testing custom logger
from xlogger import Logger

xLogger = Logger(__name__, 'info')
logger = xLogger.log #getting logging object
#---

class IMDBscraper:
    def search(self,s): #s is string input (movie name)
        s2=s.split(' ')
        s2='+'.join(s2)
        s2='https://www.google.com/search?q='+s2+'+imdb'
        r = requests.get(s2) 
        soup = BeautifulSoup(r.content, 'html5lib') 
        logger.debug(soup.prettify())
        for a in soup.find_all('a'):
            if(a.get('href')[:28]=='/url?q=https://www.imdb.com/'):
                return(a.get('href')[7:44])

    def movieDetails(self,s):
        details={}
        title=self.search(s)
        #wb.open(title)
        r = requests.get(title)
        soup = BeautifulSoup(r.content, 'lxml')
        
        #Finding name
        x=soup.find('h1')
        details['Name']=str(x.text).replace(u'\xa0',u' ').strip()
        #Finding rating
        for i in soup.find_all('span'):
            logger.debug(i.get('itemprop'))
            if(i.get('itemprop')=='ratingValue'):
                details['Rating']=float(i.string)
                break
        
        #Finding genres
        details['Genres']=[]
        for i in soup.find_all('div'):
            logger.debug(i.get('class'))
            if(i.get('class')=='see-more inline canwrap'.split()):
                x=i.find('h4')
                logger.debug('-'+x.string+'-')
                if(str(x.string)=='Genres:'):
                    #i.find_all('a')
                    for j in i.find_all('a'):
                        details['Genres'].append(j.string.strip())
                logger.debug(x.find_all('h4'))
            elif(i.get('class')=='summary_text'.split()):
                details['Summary']=i.text.strip()
            elif(i.get('class')=='credit_summary_item'.split()):
                x=(i.text.split('\n'))
                details[x[1][:len(x[1])-1]]=x[2][:len(x[2])-1].strip().split(', ')

        #downloading poster
        if not path.exists('web/images/posters'):
            makedirs('web/images/posters')
            
        poster = soup.find('div', attrs = {'class':'poster'})
        posterImg = poster.find('img')
        imgSrc = posterImg.get('src')
        logger.info('trying to download poster')
        try:
            img = requests.get(imgSrc, stream=True)
            try:
                with open('web/images/posters/'+details['Name']+'.jpg', 'wb') as fout:
                    copyfileobj(img.raw, fout)
                del img
                details['Poster'] = 'web/images/posters/'+details['Name']+'.jpg'
                logger.info('Poster downloaded')
            except:
                logger.exception('Unable to save poster')
        except:
            logger.exception('Unable to get poster')

        return(title[27:36],details)
        '''Details include
        Name
        Genres
        Rating
        Summary
        Director
        Writers
        Stars
        '''

# FOR UNIT TESTING, PLEASE IGNORE
# s=input()
# obj=IMDBscraper()
# logger.debug(obj.movieDetails(s))