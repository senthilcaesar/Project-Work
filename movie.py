#! /usr/bin/python3

MIN_NAME_LENGTH = 3
MIN_LENGTH      = 15
MAX_LENGTH      = 1000
FORMATS         = ('DVD', "Blue Ray")
FILENAME        = 'video.txt'

class Video:

         def __init__(self, name, length, format):
               self.__check_name(name)
               self.__check_length(length)
               self.__check_format(format)
               self.__collection_no = self.__next_collection_no()
               self.__name = name
               self.__length = length
               self.__format = format


         def __check_name(self, name):
               char_count = 0
               for char in name:
                    if char.isalnum():
                         char_count += 1
               if char_count < MIN_NAME_LENGTH:
                    raise ValueError('Name must have at least three characters that are letters or digits')

         def __check_length(self, length):
               if type(length) is not int:
                    raise TypeError('Video constructor expects a integer argument for length')
               if length < MIN_NAME_LENGTH or length > MAX_LENGTH:
                    raise ValueError('Length must be at least ' + str(MIN_LENGTH) +
                                     ' and no more than ' + str(MAX_LENGTH))

         def __check_format(self, format):
               if format not in FORMATS:
                    raise ValueError('Format must be one of ' + str(FORMATS))

         def __next_collection_no(self):
               try:
                  file = open(FILENAME, 'r')
                  collection_no = int(file.readline())
                  collection_no += 1
                  file.close()
                  file = open(FILENAME, 'w')
                  file.write(str(collection_no))
                  file.close()
                  return collection_no
               except:
                  collection_no = 1
                  file = open(FILENAME, 'w')
                  file.write(str(collection_no))
                  file.close()
                  return collection_no

         def __str__(self):
                return str(self.__collection_no) + ': ' + self.__name + ', ' + \
                       str(self.__length) + ' minutes, ' + self.__format

         def get_collection_no(self):
                return self.__collection_no

         def get_name(self):
                return self.__name

         def get_length(self):
                return self.__length

         def get_format(self):
                return self.__format

class Movie(Video):

         def __init__(self, name, length, format, director, studio):
               Video.__init__(self, name, length, format)
               self.__director = director
               self.__studio   = studio
               self.__actors    = []

         def get_director(self):
               return self.__director

         def get_studio(self):
               return self.__studio

         def get_actors(self):
               return self.__actors

         def add_actor(self, name):
               self.__actors.append(name)

         def __str__(self):
               return super().__str__() + ' Directed by ' + self.__director + ', ' + self.__studio


if __name__ == '__main__':
       m1 = Movie('Forbidden Planet', 100, 'DVD', 'Fred M. Wilcox', 'MGM')
       m1.add_actor('Walter Pidgeon')
       m1.add_actor('Anne Francis')
       m1.add_actor('Leslie Nielson')
       m1.add_actor('Warren Stevens')
       print(m1)
       print(m1.get_actors())

       print("isinstance(m1, Movie):", isinstance(m1, Movie))
       print("isinstance(m1, Video):", isinstance(m1, Video))
