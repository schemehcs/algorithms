import unittest
import random

class TreeNode:
    def __init__(self, v):
        self.key = v
        self.right = self.left = None
        self.p = None
        self.color = 0

    def insert(self, v):
        if self.key == v:
            raise ValueError("value collision")
        elif self.key < v:
            if self.right == None:
                n = TreeNode(v)
                n.p = self
                self.right = n
            else:
                self.right.insert(v)
        else:
            if self.left == None:
                n = TreeNode(v)
                n.p = self
                self.left = n
            else:
                self.left.insert(v)

    def insert_nonrec(self, v):
        x = self
        while True:
            if x.key == v:
                raise ValueError("key conflict {}, {}", x.key, v)
            elif x.key < v:
                if x.right:
                    x = x.right
                else:
                    x.right = TreeNode(v)
                    return
            elif x.left:
                x = x.left
            else:
                x.left = TreeNode(v)
                return 

    def inorder(self, f):
        if self.left != None:
            self.left.inorder(f)
        f(self)
        if self.right != None:
            self.right.inorder(f)

    def inorder_nonrec(self, f):
        stack = []
        stack.append(self)
        while stack:
            n = stack.pop()
            if n.color == 0:
                if n.right != None:
                    stack.append(n.right)
                n.color = 1
                stack.append(n)
                if n.left != None:
                    stack.append(n.left)
            else:
                f(n.key)
    
    def preorder(self, f):
        f(self.key)
        if self.left != None:
            self.left.preorder(f)
        if self.right != None:
            self.right.preorder(f)

    def preorder_nonrec(self, f):
        stack = []
        stack.append(self)
        while stack:
            n = stack.pop()
            if n.r != None:
                stack.append(n.r)
            if n.l != None:
                stack.append(n.l)
            f(n.v)

    def postorder(self, f):
        if self.left != None:
            self.left.postorder(f)
        if self.right != None:
            self.right.postorder(f)
        f(self.key)

    def postorer_nonrec(self, f):
        stack = []
        self.color = 0
        stack.append(self)
        while stack:
            n = stack.pop()
            if n.color == 0:
                n.color = 1
                if n.r:
                    n.r.color = 0
                    stack.append(n.r)
                if n.l:
                    n.l.color = 0
                    stack.append(n.l)
                stack.append(n)
            if n.color == 1:
                f(n.v)

    def min(self):
        n = self
        while n.left:
            n = n.left
        return n

    def max(self):
        n = self
        while n.right:
            n = n.right

    def predcessor(self):
        if self.left != None:
            return self.left.max()
        x = self
        y = x.p
        while y and x == y.right:
            x = y
            y = y.p
        return None

    def succesor(self):
        if self.right != None:
            return self.right.min()
        x = self
        y = x.p
        while y and x == y.left:
            x = y
            y = y.p
        return None


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, v):
        if self.root == None:
            self.root = TreeNode(v)
        else:
            self.root.insert(v)

    def transplant(self, u, v):
        if u.p is None:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v:
            v.p = u.p
        
    def delete(self, u):
        if not u.left:
            self.transplant(u, u.right)
        elif not u.right:
            self.transplant(u, u.left)
        else:
            y = u.right.min()
            if y != u.right:
                self.transplant(y, y.right)
                y.right = u.right
                y.right.p = y
            self.transplant(u, y)
            y.left = u.left
            y.left.p = y

class Tests(unittest.TestCase):
    def test_binary_tree(self):
        tree = Tree()
        ls = []
        for _ in range(20):
            tree.insert(random.randrange(1000))
        if tree.root:
            tree.root.inorder(lambda v: ls.append(v))
        print(list(map(lambda n: n.key, ls)))
        for n in ls[:-1]:
            tree.delete(n)
        if tree.root:
            print(tree.root.key)

if __name__ == '__main__':
    unittest.main()

