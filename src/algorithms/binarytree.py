class TreeNode:
    def __init__(self, v):
        self.key = v
        self.right = self.left = None
        self.p = None

    # O(h) time, where h is the tree height.
    def insert(self, v):
        if self.key == v:
            raise ValueError("value collision")
        elif self.key < v:
            if self.right is None:
                n = TreeNode(v)
                n.p = self
                self.right = n
            else:
                self.right.insert(v)
        else:
            if self.left is None:
                n = TreeNode(v)
                n.p = self
                self.left = n
            else:
                self.left.insert(v)

    # O(h) time, where h is the tree height.
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
                    x.right.p = x
                    return
            elif x.left:
                x = x.left
            else:
                x.left = TreeNode(v)
                x.left.p = x
                return

    # O(n) time and O(h) recursion space.
    def inorder(self, f):
        if self.left is not None:
            self.left.inorder(f)
        f(self)
        if self.right is not None:
            self.right.inorder(f)

    # O(n) time and O(h) stack space.
    def inorder_nonrec(self, f):
        stack = []
        node = self
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            f(node.key)
            node = node.right

    # O(n) time and O(h) recursion space.
    def preorder(self, f):
        f(self.key)
        if self.left is not None:
            self.left.preorder(f)
        if self.right is not None:
            self.right.preorder(f)

    # O(n) time and O(h) stack space.
    def preorder_nonrec(self, f):
        stack = []
        stack.append(self)
        while stack:
            n = stack.pop()
            f(n.key)
            if n.right is not None:
                stack.append(n.right)
            if n.left is not None:
                stack.append(n.left)

    # O(n) time and O(h) recursion space.
    def postorder(self, f):
        if self.left is not None:
            self.left.postorder(f)
        if self.right is not None:
            self.right.postorder(f)
        f(self.key)

    # O(n) time and O(h) stack space.
    def postorder_nonrec(self, f):
        stack = [(self, False)]
        while stack:
            node, visited = stack.pop()
            if visited:
                f(node.key)
            else:
                stack.append((node, True))
                if node.right is not None:
                    stack.append((node.right, False))
                if node.left is not None:
                    stack.append((node.left, False))

    def postorer_nonrec(self, f):
        self.postorder_nonrec(f)

    # O(h) time.
    def min(self):
        n = self
        while n.left:
            n = n.left
        return n

    # O(h) time.
    def max(self):
        n = self
        while n.right:
            n = n.right
        return n

    # O(h) time.
    def predcessor(self):
        if self.left is not None:
            return self.left.max()
        x = self
        y = x.p
        while y and x == y.left:
            x = y
            y = y.p
        return y

    # O(h) time.
    def succesor(self):
        if self.right is not None:
            return self.right.min()
        x = self
        y = x.p
        while y and x == y.right:
            x = y
            y = y.p
        return y


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, v):
        if self.root is None:
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

    # O(h) time.
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
