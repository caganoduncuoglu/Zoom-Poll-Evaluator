class Student:

    def __init__(self,number,name,surname,description,submissions=[]):
        self.__number=number
        self.__name=name
        self.__surname=surname
        self.__description=description
        self.__submissions=submissions