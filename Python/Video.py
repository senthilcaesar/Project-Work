#! /usr/bin/python3

MIN_NAME_LENGTH = 3
MIN_LENGTH      = 15
MAX_LENGTH      = 1000
FORMATS         = ('DVD', "Blue Ray")
FILENAME        = 'video.txt'

# A superclass for all videos
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
            except FileNotFoundError:
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



if __name__ == '__main__':
     v1 = Video('Forbidden Planet', 100, 'DVD')
     print(v1)
