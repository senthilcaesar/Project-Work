class Node:
    def __init__(self, data, label):
        self.left = None
        self.right = None
        self.data = data
        self.label = label
    
    def insert(self, data, label):
        if self.data:
            if data > self.data:
                if self.right == None:
                    self.right = Node(data, label)
                else:
                    self.right.insert(data, label)
            elif data < self.data:
                if self.left == None:
                    self.left = Node(data, label)
                else:
                    self.left.insert(data, label)
        else:
            self.data = data
        
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data, self.label)
        if self.right:
            self.right.PrintTree()
            
    def get_height(self, node):
        if node is None: return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def get_diameter(self, node):
        if node is None: return 0
        lh = self.get_height(node.left)
        rh = self.get_height(node.right)
        ld = self.get_diameter(node.left)
        rd = self.get_diameter(node.right)
        return max(lh+rh+1, max(ld+1, rd+1))
    
    ''' Breath - First Serarch '''
    def level_order_traversal(self, node):
        h = self.get_height(node)
        for i in range(1, h+1):
            self.printLevel(root, i)
    
    def DFS_setParent(self, node, parent):
        if node == None: return 0
        if node.left:
            if node.left not in parent:
                parent[node.left] = node
        if node.right:
            if node.right not in parent:
                parent[node.right] = node
        self.DFS_setParent(node.left, parent)
        self.DFS_setParent(node.right, parent)
    
    ''' DFS Inorder Traversal '''
    def DFS_vist_allPath(self, node, stack):
        if node == None: return 0
        stack.append(node)
        self.DFS_vist_allPath(node.left, stack)
        if node.left == None and node.right == None:
            for n in stack:
                print(n.data, end=" ")
            print()
        self.DFS_vist_allPath(node.right, stack)
        stack.pop()
        
    def printLevel(self, root , level):
        if root is None:
            return
        if level == 1:
            print(root.data, end = "  ")
        elif level > 1 :
            self.printLevel(root.left , level-1)
            self.printLevel(root.right , level-1)
        
root = Node(9,1)
root.insert(6, 1)
root.insert(12, 1)
root.insert(4, 1)
root.insert(7, 1)
root.insert(11, 1)
root.insert(13, 1)

lh = root.get_height(root.left)
rh = root.get_height(root.right)
parent = {}
stack = []
print("Left Tree Height = ", lh)
print("Right Tree Height = ", rh)
print("Tree Diameter = ", root.get_diameter(root))
print(" ")
print("Level Order Traversal")
root.level_order_traversal(root)
root.DFS_setParent(root, parent)
print("\n")
print("All root-to-leaf paths")
root.DFS_vist_allPath(root, stack)
