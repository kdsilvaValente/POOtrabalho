from run import getconnection 
from fuzzywuzzy import fuzz

class Search:
    def __init__(self):
        self.music_collection = getconnection.get_collection("Musica")
        self.minimum_similarity = 70
    def get_singers(self, singer_name):
        results=[]
        for document in self.music_collection.find({}):     
            document_title=document.get("titulo")
            similarity_nivel= fuzz.partial_ratio(singer_name.lower(), document_title.lower())
            if similarity_nivel >= self.minimum_similarity:
                results.append((document_title, similarity_nivel))
                print(document_title)


    def get_title(self):
        pass
    def get_by_producer(self):
        pass
    def get_by_composer(self):
        pass


teste= Search()
teste.get_singers("welcasome to nesw york")