from Node import Node  # Import the Node class

class AVLTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def rotate_right(node):
        if node is None:
            return node
        tmp = node.left
        node.left = tmp.right
        if tmp.right is not None:
            tmp.right.parent = node
        tmp.right = node
        tmp.parent = node.parent
        node.parent = tmp

        node.update_height()
        tmp.update_height()
        return tmp

    @staticmethod
    def rotate_left(node):
        if node is None:
            return node
        tmp = node.right
        node.right = tmp.left
        if tmp.left is not None:
            tmp.left.parent = node
        tmp.left = node
        tmp.parent = node.parent
        node.parent = tmp

        node.update_height()
        tmp.update_height()
        return tmp

    @staticmethod
    def __insert(node, key, parent=None):
        if node is None:
            return Node(key, parent)
        if key < node.key:
            node.left = AVLTree.__insert(node.left, key, node)
        elif key > node.key:
            node.right = AVLTree.__insert(node.right, key, node)
        else:
            return node
        node.update_height()
        balance = node.get_balance()
        if balance > 1:
            if key < node.left.key:
                return AVLTree.rotate_right(node)
            else:
                node.left = AVLTree.rotate_left(node.left)
                return AVLTree.rotate_right(node)
        elif balance < -1:
            if key > node.right.key:
                return AVLTree.rotate_left(node)
            else:
                node.right = AVLTree.rotate_right(node.right)
                return AVLTree.rotate_left(node)
        return node

    def insert(self, key):
        self.root = AVLTree.__insert(self.root, key)

    @staticmethod
    def __delete(node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = AVLTree.__delete(node.left, key)
        elif key > node.key:
            node.right = AVLTree.__delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            succ = AVLTree.min_value_node(node.right)
            node.key = succ.key
            node.right = AVLTree.__delete(node.right, succ.key)

        if node is None:
            return node

        node.update_height()
        balance = node.get_balance()
        if balance > 1:
            if node.left.get_balance() >= 0:
                return AVLTree.rotate_right(node)
            else:
                node.left = AVLTree.rotate_left(node.left)
                return AVLTree.rotate_right(node)
        elif balance < -1:
            if node.right.get_balance() <= 0:
                return AVLTree.rotate_left(node)
            else:
                node.right = AVLTree.rotate_right(node.right)
                return AVLTree.rotate_left(node)
        return node

    def delete(self, key):
        self.root = AVLTree.__delete(self.root, key)

    @staticmethod
    def __search(root, key):
        if root is None or root.key == key:
            return root
        if root.key < key:
            return AVLTree.__search(root.right, key)
        return AVLTree.__search(root.left, key)

    def search(self, key):
        return AVLTree.__search(self.root, key)

    @staticmethod
    def min_value_node(node):
        current_node = node
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    @staticmethod
    def max_value_node(node):
        if node is None or node.right is None:
            return node
        return AVLTree.max_value_node(node.right)

    def inorder_traversal(self, node=None, result=None):
        if node is None:
            node = self.root
            result = []
        if node.left is not None:
            self.inorder_traversal(node.left, result)
        result.append(node.key)
        if node.right is not None:
            self.inorder_traversal(node.right, result)
        return result

    def find(self, key):
        return self._find(self.root, key)

    @staticmethod
    def _find(node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return AVLTree._find(node.left, key)
        return AVLTree._find(node.right, key)

    def predecessor(self, key):
        node = self.find(key)
        if not node:
            return None
        if node.left:
            return AVLTree.max_value_node(node.left).key
        p = node.parent
        while p is not None and node == p.left:
            node = p
            p = p.parent
        if p:
            return p.key
        else:
            return None

    def successor(self, key):
        node = self.find(key)
        if not node:
            return None
        if node.right:
            return AVLTree.min_value_node(node.right).key
        p = node.parent
        while p is not None and node == p.right:
            node = p
            p = p.parent
        if p:
            return p.key
        else:
            return None
