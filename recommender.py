from nltk import word_tokenize as words
import app

class recommender:
    def findSimilar(self,id,details):
        counts=[0]*3
        movie=['']*3
        curr=0
        d=['Genres','Director','Writers','Stars']
        for i in details:
            for j in d:
                curr+=len(set(details[id][j]).intersection(set(details[i][j])))   
            #summ=word(details[i]['Summary']) #For summary
            j=0
            while(counts[j]>curr):
                j+=1
            if(j<3):
                counts.insert(j,curr)
                movie.insert(j,curr)
        return(movie[:5])
        
