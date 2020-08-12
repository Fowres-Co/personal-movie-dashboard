import webbrowser as wb
from bs4 import BeautifulSoup
import requests
class IMDBscraper:
    def search(self):
        s=input("Enter the name of the movie: ")
        s2=s.split(' ')
        s2='%20'.join(s2)
        s2='https://www.imdb.com/find?q='+s2+'&s=tt&ttype=ft&ref_=fn_ft'
        r = requests.get(s2) 
        soup = BeautifulSoup(r.content, 'html5lib') 
        
        #table = soup.find('div', attrs = {'class':'container'}) 
        for link in soup.find_all('a'):
            #print(link.get('href'),str(link.string).lower())
            if((str(link.string)).lower()==s.lower()):
                relative=(link.get('href'))
                absolute='https://www.imdb.com'+relative
                return(absolute)
        #print(s2)

    def movieDetails(self):
        details={}
        title=self.search()
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
        print(details)


obj=IMDBscraper()
obj.movieDetails()
