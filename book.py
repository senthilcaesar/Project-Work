# Create a new class called Book
class Book:

        # Constructor Intialization
        def __init__(self, title, sub_title, author, publisher, copyright):
                self.__title = title
                self.__sub_title = sub_title
                self.__author = author
                self.__publisher = publisher
                self.__copyright = copyright
                self.__description = ''

        # Getters and Setters to access and mutate the fields
        def get_title(self):
                return self.__title

        def get_sub_title(self):
                return self.__sub_title

        def get_author(self):
                return self.__author

        def get_publisher(self):
                return self.__publisher

        def get_copyright(self):
                return self.__copyright

        def set_description(self, description):
                self.__description = description

        def get_description(self):
                return self.__description

        def __str__(self):
                return self.__title + ' ' + self.__sub_title +  ' ' + self.__author + ' ' + self.__publisher + ' ' + self.__copyright

data_file = open('book.txt', 'r')
line = data_file.readline()

# Read each line of the file and assign it to the field
counter = 1
while line:
        if   counter == 1:
                title = line
        elif counter == 2:
                sub_title = line
        elif counter == 3:
                author = line
        elif counter == 4:
                publisher = line
        elif counter == 5:
                copyright = line
        else:
                description = line
        counter = counter + 1
        line = data_file.readline()
data_file.close()


b1 = Book(title, sub_title, author, publisher, copyright)
b1.set_description(description)
print('Title:', b1.get_title())
print('Sub_title:', b1.get_sub_title())
print('Author:', b1.get_author())
print('Publisher:', b1.get_publisher())
print('Copyright:', b1.get_copyright())
print('Description:', b1.get_description())
print(b1)
