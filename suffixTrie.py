class TrieNode:
    
    def __init__(self):
        self.childrens = {}
        self.isFinal = False
        self.prefixCount = 0
        
    def createChild(self, char):
        node = TrieNode()
        self.childrens[char] = node
        return node
    
    def childCount(self):
        return len(self.childrens)
    
    def uniqueWords(self):
        return self.prefixCount
        
    def getOrCreateChild(self, char):
        if char in self.childrens:
            return self.childrens[char]
        else:
            return self.createChild(char)
                                    
class suffixTrie:
    
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        node.prefixCount += 1
        word = list(word)
        for c in word:
            node = node.getOrCreateChild(c)
            node.prefixCount += 1
        node.isFinal = True
      
    def hasSubstring(self, word):
        node = self.root
        words = list(word)
        for c in words:
            if c in node.childrens:
                node = node.childrens[c]
            else:
                node = None               
            if node == None:
                return False
        return True
        
    def checkSuffix(self, word):
        node = self.root
        words = list(word)
        for c in words:
            if c in node.childrens:
                node = node.childrens[c]
        for key in node.childrens:
            if key == '$':
                return True
            else:
                return False
            
    def countSubstringOccurence(self, word, string):
        if self.hasSubstring(word) == True:
            node = self.root       
            words = list(word)
            for c in words:
                if c in node.childrens:
                    node = node.childrens[c]
            count = node.prefixCount
            print("Number of times substring", word, "occurs in", string, " = ", count)
        else:
            print(word, "is not a substring of", string)
               
    def isSuffix(self, word, string):
           if self.checkSuffix(word) == True:
               print(word, "is a suffix of", string)
           else:
               print(word, "is not a suffix of", string)              
                
    def isSubstring(self, word, string):
           if self.hasSubstring(word) == True:
               print(word, "is a substring of", string)
           else:
               print(word, "is not a substring of", string)
               
    def traverse(self, node):
        for key in node.childrens:
            print(key, end="")
            child = node.childrens[key]
            self.printChild(child)
            
    def printChild(self, child):
        for key in child.childrens:
            print(key, end="")
            descend = child.childrens[key]
            self.traverse(descend)
            
suffix_trie = suffixTrie()
suffixes = []
string = 'ABAABA'
given = string+'$'
length = len(given)

for i in range(length-1, -1, -1):
    suffixes.append(given[i:length])

for words in suffixes:
    suffix_trie.insert(words)
    
suffix_trie.isSubstring("BAAB", string)
suffix_trie.isSuffix("BAAB", string)
suffix_trie.isSubstring("BAB", string)
suffix_trie.isSuffix("AABA", string)
suffix_trie.countSubstringOccurence("ABA", string)
suffix_trie.traverse(suffix_trie.root)
