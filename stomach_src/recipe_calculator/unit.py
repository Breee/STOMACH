class Unit(object):

    def __init__(self,id,language,name,short,to_gram_factor,to_millilitres_factor):
        self.__id = id
        self.__language = language
        self.__name = name
        self.__short = short
        self.__to_gram_factor = to_gram_factor
        self.__to_millilitres_factor = to_millilitres_factor

    def get_id(self):
        return self.__id

    def get_language(self):
        return self.__language

    def get_name(self):
        return self.__name

    def get_short(self):
        return self.__short

    def get_to_gram_factor(self):
        return self.__to_gram_factor

    def get_to_millilitres_factor(self):
        return self.__to_millilitres_factor

    def __str__(self):
        return "%s(%d)"%(self.get_name(),self.get_id())
