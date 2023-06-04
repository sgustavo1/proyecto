class BPlusTree:
    def __init__(self, order):
        # Constructor del árbol B+-Tree
        # Time complexity: O(1)
        # Space complexity: O(1)
        self.root = BPlusNode(order)
        self.order = order

    def insert(self, key, value):
        # Inserta una clave-valor en el árbol B+-Tree
        # Time complexity: O(log n)
        # Space complexity: O(log n)
        self.root.insert(key, value)

    def range_search(self, start, end):
        # Realiza una búsqueda de rango en el árbol B+-Tree
        # Time complexity: O(log n + k)
        # Space complexity: O(k)
        results = []
        node = self.find_leaf(start)

        while node is not None:
            for i in range(len(node.keys)):
                if node.keys[i] >= start and node.keys[i] <= end:
                    results.append(node.values[i])

            node = node.next

        return results

    def find_leaf(self, key):
        # Encuentra la hoja que contiene la clave especificada
        # Time complexity: O(log n)
        # Space complexity: O(1)
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys):
                if key < node.keys[i]:
                    break
                i += 1
            node = node.children[i]
        return node


class BPlusNode:
    def __init__(self, order):
        # Constructor del nodo del árbol B+-Tree
        # Time complexity: O(1)
        # Space complexity: O(order)
        self.keys = []
        self.values = []
        self.children = []
        self.is_leaf = True
        self.order = order
        self.next = None

    def insert(self, key, value):
        # Inserta una clave-valor en el nodo del árbol B+-Tree
        # Time complexity: O(log n)
        # Space complexity: O(log n)
        if key in self.keys:
            index = self.keys.index(key)
            self.values[index].append(value)
        else:
            index = self.find_insert_index(key)
            self.keys.insert(index, key)
            self.values.insert(index, [value])

        if len(self.keys) > self.order:
            self.split()

    def find_insert_index(self, key):
        # Encuentra la posición de inserción de una clave en el nodo
        # Time complexity: O(log n)
        # Space complexity: O(1)
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1
        return index

    def split(self):
        # Divide el nodo en dos nodos y realiza la redistribución de claves y valores
        # Time complexity: O(log n)
        # Space complexity: O(log n)
        mid = (len(self.keys) + 1) // 2
        new_node = BPlusNode(self.order)

        new_node.keys = self.keys[mid:]
        new_node.values = self.values[mid:]
        new_node.children = self.children[mid:]
        new_node.is_leaf = self.is_leaf
        new_node.next = self.next

        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        self.children = self.children[:mid]
        self.next = new_node

        if not self.is_leaf:
            new_node.is_leaf = False

        parent = None
        if self.is_leaf:
            new_node.is_leaf = True

        if parent is not None:
            self.keys = parent.keys
            self.values = parent.values
            self.children = parent.children
            self.next = parent.next
            self.is_leaf = parent.is_leaf

    def __str__(self):
        return str(self.keys)
