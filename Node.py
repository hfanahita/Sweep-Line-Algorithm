class Node:
    def __init__(self, key, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 1

    def update_height(self):
        self.height = 1 + max(self.get_height(self.left), self.get_height(self.right))

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self):
        return self.get_height(self.left) - self.get_height(self.right)
