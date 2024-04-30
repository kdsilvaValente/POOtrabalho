from run import getconnection 
from fuzzywuzzy import fuzz

class Search:
    def __init__(self):
        self.music_collection = getconnection.get_collection("Musica")
        self.minimum_similarity = 70


    def get_by_type(self, type,name_search):#recebe o nome do que você está pesquisando e o onde procurar no banco
        results=[]
        for document in self.music_collection.find({}):     
            document_title=document.get(type)
            document_title = str(document_title) 
            similarity_nivel= fuzz.partial_ratio(name_search.lower(), document_title.lower())
            if similarity_nivel >= self.minimum_similarity:
                results.append((document))
                print(results)
                return results
    
