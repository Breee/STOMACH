class Category(object):

    def __init__(self, id, name, language):
        self.__id = id
        self.__name = name
        self.__language = language

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_language(self):
        return self.__language

    def __str__(self):
        return self.__name
