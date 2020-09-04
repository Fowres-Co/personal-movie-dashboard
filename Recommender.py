from nltk import word_tokenize as words
class Recommender:
    def findSimilar(self,id,details):
        counts=[0]*3
        movie=['']*3
        curr=0
        attr=['Genres','Director','Writer','Star']
        for i in details:
            #print(details[i].keys())
            for j in attr:
                curr+=len(set(details[id][j]).intersection(set(details[i][j])))   
            #summ=word(details[i]['Summary']) #For summary
            j=0
            while(counts[j]>curr):
                j+=1
            if(j<3):
                counts.insert(j,curr)
                movie.insert(j,details[i])
        return(movie[:3],counts[:3]) #details of most similar movies returned

        
