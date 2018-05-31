from BinaryNode import BinaryNode
import random
from time import time

class BinaryTree:
    
    def __init__(self):
        ''' Create empty binary tree '''
        self.root = None
        
    def add(self, value):
        ''' Insert into Binary Tree '''
        if self.root is None:
            self.root = BinaryNode(value)            
        else:
            self.root.add(value)    
        ''' AVL Balancing tree section '''
#        self.update_balance(self.root)
#        node = self.get_node(value, self.root)
#        print("Last added Node = ", node.value)
#        node = self.traverseLeaf(node)
#        if node != None:
#            self.reBalance(node)
      
    def deepestNode(self, node):
        h = self.get_height(node)
        #for i in range(1, h+1):
        self.find_deepest(node, h)
        self.find_rightmost_deepest(node, h)
            
    ''' Finding the deepest node is an unbalanced binary tree '''
    def find_deepest(self, root, level):
        if root is None:
            return
        if level == 1:
            print("Deepest node in an unbalanced binary tree: ", root.value)
        elif level > 1:
            self.find_deepest(root.left, level-1)
            self.find_deepest(root.right, level-1)
    
    ''' Finding the right most element in the lowest level in an unbalanced binary tree '''
    def find_rightmost_deepest(self, root, level):
        if root is None:
            return
        if level == 1:
            if root.value > root.parent.value:
                print("Right most element in the lowest level in an unbalanced binary tree: ", root.value)
        elif level > 1:
            self.find_rightmost_deepest(root.left, level-1)
            self.find_rightmost_deepest(root.right, level-1)
            
    def traverseLeaf(self, node):      
        if node.balance == -2 or node.balance == 2: 
            print("Return Node", node.value, "Balance = ", node.balance)
            return node
        elif node.value == node.parent.value: 
            return None
        else:
            node = node.parent
            return self.traverseLeaf(node)
            
    def update_balance(self, node):
        if node == None: return 0       
        l_h = self.get_height(node.left)
        r_h = self.get_height(node.right)
        node.balance = r_h - l_h
        self.update_balance(node.left)
        self.update_balance(node.right)
     
    def reBalance(self, node):
        if node.balance < -1:
            if node.left.balance == -1 or node.left.balance == 0:
                self.rightRotation(node)
                print("Perform Right rotation around: " , node.value);
                return True
                
            if node.left.balance == 1:
                self.leftRotation(node.left)
                self.rightRotation(node)
                print("Perform LeftRight rotation around: " , node.value);
                return True
                
        elif node.balance > 1:
            if node.right.balance == 1 or node.right.balance == 0:
                self.leftRotation(node)
                print("Perform left rotation around: " , node.value);
                return True
                
            if node.right.balance == -1:
                if node.right.left.balance == 1:
                    self.leftRotation(node.right.left)
                print("Peforming RightLeft rotation around: ", node.value)
                self.rightRotation(node.right)
                self.leftRotation(node)
                
                return True
                
    def rightRotation(self, node):
        newroot = node.left
        newroot.parent = node.parent
        if newroot.right != None:
            newroot.parent.left = newroot.right
            node.parent.parent = newroot
            newroot.right = node
            #node.parent = newroot
        else:
            newroot.right = node
            node.parent = newroot
        
        if newroot.parent.value == node.value:
            newroot.parent = newroot
            self.root = newroot
            if node.right == None:
                node.left = None
        else:
            if newroot.parent.value < newroot.right.value:
                newroot.parent.right = newroot
                newroot.right.left = None 
            else:
                newroot.parent.left = newroot
                newroot.left.right = None
                
        self.update_balance(self.root)
       
    def leftRotation(self, node):
        newroot = node.right
        newroot.parent = node.parent
        if newroot.left != None:
            node.parent.right = newroot.left
            node.parent.parent = newroot
            newroot.left = node
            #node.parent = newroot
        else:
            newroot.left = node
            node.parent = newroot
 
        if newroot.parent.value == node.value:
            newroot.parent = newroot
            self.root = newroot
            if node.left == None:
                node.right = None
        else:
            if newroot.parent.value < newroot.left.value:
                newroot.parent.right = newroot
                newroot.left.right = None
            else:
                newroot.parent.left = newroot
                newroot.left.right = None
        self.update_balance(self.root)
                    
    def contains(self, target):
        ''' check whether BST contains target value '''
        node = self.root
        while node:
            if target == node.value:
                return True
            if target < node.value:
                node = node.left
            else:
                node = node.right
        
        return False
    
    def performance(self):
        n = 1024
        while n <= 65536:
            bt = BinaryTree()
            for i in range(n):
                bt.add(random.randint(1, n))
            now = time()
            bt.contains(random.randint(1, n))
            time_taken = (time() - now) * 1000
            print(n, time_taken)
            n *= 2
      
    def get_height(self, node):
        if node is None: return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def Inorder(self, node):
        if node is None: return 0
        self.Inorder(node.left)
        print(node.value, end=" ")
        self.Inorder(node.right)
        
    def Preorder(self, node):
        if node is None: return 0
        print(node.value, end=" ")
        self.Preorder(node.left)
        self.Preorder(node.right)
        
    def Print_balance(self, node):
        if node is None: return 0
        print(node.balance, end=" ")
        self.Print_balance(node.left)
        self.Print_balance(node.right)
        
    def Postorder(self, node):
        if node is None: return 0
        self.Postorder(node.left)
        self.Postorder(node.right)
        print(node.value, end=" ")
        
    def Levelorder(self, node):
        h = self.get_height(node)
        for i in range(1, h+1):
            self.printLevel(self.root, i)
        
    def printLevel(self, root, level):
        if root is None:
            return
        if level == 1:
            print(root.value, end = "  ")
        elif level > 1 :
            self.printLevel(root.left , level-1)
            self.printLevel(root.right , level-1)
            
    ''' DFS Inorder Traversal '''
    def DFS_allPath(self, node, stack):
        if node is None: return 0
        stack.append(node)
        self.DFS_allPath(node.left, stack)
        if node.left == None and node.right == None:
            for n in stack:
                print(n.value, end=" ")
            print()
        self.DFS_allPath(node.right, stack)
        stack.pop()
     
    def get_node(self, value, root):
        node = root       
        while node:
            if value == node.value:
                return node
            if value < node.value:
                node = node.left
            else:
                node = node.right
        
        return False
    
    def find_min(self, node, stack):
        if node is None: return 0
        stack.append(node.value)
        self.find_min(node.left, stack)
        self.find_min(node.right, stack)
        return int(min(stack))
            
    def remove(self, root, value):
        node = self.get_node(value, root)
        if node:
            ''' Node is a leaf '''
            if node.left == node.right == None:
                if node.parent.value > node.value:
                    node.parent.left = None
                    #node = None
                else:
                    traverse = node.parent
                    node.parent.right = None
                    #node = None
            self.update_balance(self.root)
            node = self.traverseLeaf(traverse)
            if node != None:
                self.reBalance(node)
            return node
        
            ''' Node with 1 left child '''
            if node.left and node.right is None:
                if node.value > node.parent.value:
                    node.parent.right = node.left
                    node.left.parent = node.parent
                    node = None
                else:
                    node.parent.left = node.left
                    node.left.parent = node.parent
                    node = None
                return node.parent
            
            ''' Node with 1 right child '''        
            if node.right and node.left is None:
                if node.value < node.parent.value:
                    node.parent.left = node.right
                    node.right.parent = node.parent
                    node = None
                else:
                    node.parent.right = node.right
                    node.right.parent = node.parent
                    node = None
                return node
            
            ''' Node has 2 childs ''' 
            stack = []
            if node.left and node.right:
                min_node = self.find_min(node.right, stack)
                min_node = self.get_node(min_node, node.right)
                node.value = min_node.value               
                self.remove(node.right, min_node.value)                
        
        else:
            print("Invalid Node")             
                
        self.update_balance(self.root)
        self.reBalance(self.root) 
