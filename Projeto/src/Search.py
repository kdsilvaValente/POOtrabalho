from run import getconnection 
from fuzzywuzzy import fuzz

class Search:
    def __init__(self,collection):
        self.music_collection = getconnection.get_collection(collection)
        self.minimum_similarity = 70


    def get_by_type(self, type,search):#recebe o nome do que você está pesquisando e o onde procurar no banco
        results=[]
        for document in self.music_collection.find({}):  
            document_title=document.get(type)
            if isinstance(search,int): #procurando números
                search=str(search)
                document_title=str(document_title)
                similarity_nivel= fuzz.partial_ratio(search, document_title)
                if similarity_nivel >= self.minimum_similarity:
                    results.append((document))
            else:
                document_title = str(document_title)  #procurando apenas strings
                similarity_nivel= fuzz.partial_ratio(search.lower(), document_title.lower())
                if similarity_nivel >= self.minimum_similarity:
                    results.append((document))
            
        return results
    def get_by_id(self,id):
        results=[]
        results=self.music_collection.find_one({"_id": id})
        return results

       
    


teste=Search("ALBUM")