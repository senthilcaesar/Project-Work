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
