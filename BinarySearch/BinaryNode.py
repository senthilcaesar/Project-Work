class BinaryNode:
    
    def __init__(self, value):
        ''' Create binary node '''
        self.value = value
        self.left = None
        self.right = None
        self.parent = self
        self.balance = 0
        
    def add(self, val):
        if val <= self.value:
            if self.left:
                self.left.add(val)
            else:
                self.left = BinaryNode(val)
                self.left.parent = self
        else:
            if self.right:
                self.right.add(val)
            else:
                self.right = BinaryNode(val)
                self.right.parent = self

