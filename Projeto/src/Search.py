from run import getconnection 
from fuzzywuzzy import fuzz

class Search:
    def __init__(self,collection)->None:
        """
        :param collection: nome da coleção que onde deve ser feita a pesquisa
        """
        self.music_collection = getconnection.get_collection(collection) #reponsável por realizar a conexao com a collection 
        self.minimum_similarity = 70 #taxa mínima de similariedade para retornar na pesquisa


    def get_by_type(self, type: str,search: str)-> list[dict[str, str]]:
        """
        :param type: define o campo na collection que deve ser usado para realizar a pesquisa
        :param search: define o texto buscado

        faz uma pesquisa com base no texto inserido pelo usuário retornando todos os resultados semelhantes
        """
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
    def get_by_id(self,id)-> list[dict[str, str]]:

        """
        :param id: id para buscar no banco de dados

        realiza a pesquisa no banco de dados de um id específico
        """
        
         #pesquisa um objeto com base no id
        results=[]
        results=self.music_collection.find_one({"_id": id})
        return results

       
    


