import webbrowser as wb
from bs4 import BeautifulSoup
import requests
class IMDBscraper:
    def search(self,s,year,ty): #s is string input (movie name)
        s2=s.split(' ')
        s2='+'.join(s2)
        s2='https://www.imdb.com/search/title/?title='+s2
        if(ty>0):
            s2=s2+'&title_type='
            if(ty==1):
                s2=s2+'feature,tv_movie'
            if(ty==2):
                s2=s2+'tv_series,tv_episode,tv_special,tv_miniseries'
        if(year):
            s2=s2+'&release_date='+year+'-01-01,'
        r = requests.get(s2) 
        soup = BeautifulSoup(r.content, 'html5lib') 
        
        #table = soup.find('div', attrs = {'class':'container'}) 
        for link in soup.find_all('a'):
            #print(link.get('href'),str(link.string).lower())
            if((str(link.string)).lower()==s.lower()):
                relative=(link.get('href'))
                absolute='https://www.imdb.com'+relative
                return(absolute,relative[7:16])
        #print(s2)

    def movieDetails(self,s,year,ty): #s is movie name, ty is 1-movie 2-tv series
        details={}
        title,rel=self.search(s,year,ty)
        #wb.open(title)
        r = requests.get(title)
        soup = BeautifulSoup(r.content, 'html5lib')
        
        #Finding rating
        for i in soup.find_all('span'):
            #print(i.get('itemprop'))
            if(i.get('itemprop')=='ratingValue'):
                details['Rating']=float(i.string)
                break
        
        #Finding genres
        details['Genres']=[]
        for i in soup.find_all('div'):
            #print(i.get('class'))
            if(i.get('class')=='see-more inline canwrap'.split()):
                x=i.find('h4')
                #print('-'+x.string+'-')
                if(str(x.string)=='Genres:'):
                    #i.find_all('a')
                    for j in i.find_all('a'):
                        details['Genres'].append(j.string.strip())
                #print(x.find_all('h4'))
        return(rel,details)

'''FOR UNIT TESTING, PLEASE IGNORE
s=input()
year=input()
ty=int(input())
obj=IMDBscraper()
print(obj.movieDetails(s,year,ty))'''
