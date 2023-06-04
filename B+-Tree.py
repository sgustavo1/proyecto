class BPlusTree:
    def __init__(self, order):                           # Time complexity: O(1), Space complexity: O(1)
        self.root = BPlusNode(order)
        self.order = order

    def insert(self, key, value):                         # Time complexity: O(log n), Space complexity: O(log n)
        self.root.insert(key, value)

    def range_search(self, start, end):                   # Time complexity: O(log n + k), Space complexity: O(k)
        results = []
        node = self.find_leaf(start)

        while node is not None:                           # Time complexity: O(k), Space complexity: O(1)
            for i in range(len(node.keys)):               # Time complexity: O(k), Space complexity: O(1)
                if node.keys[i] >= start and node.keys[i] <= end:
                    results.append(node.values[i])

            node = node.next

        return results

    def find_leaf(self, key):                             # Time complexity: O(log n), Space complexity: O(1)
        node = self.root
        while not node.is_leaf:                           # Time complexity: O(log n), Space complexity: O(1)
            i = 0
            while i < len(node.keys):                     # Time complexity: O(log n), Space complexity: O(1)
                if key < node.keys[i]:
                    break
                i += 1
            node = node.children[i]
        return node


class BPlusNode:
    def __init__(self, order):                            # Time complexity: O(1), Space complexity: O(order)
        self.keys = []
        self.values = []
        self.children = []
        self.is_leaf = True
        self.order = order
        self.next = None

    def insert(self, key, value):                          # Time complexity: O(log n), Space complexity: O(log n)
        if key in self.keys:                               # Time complexity: O(log n), Space complexity: O(1)
            index = self.keys.index(key)
            self.values[index].append(value)
        else:
            index = self.find_insert_index(key)            # Time complexity: O(log n), Space complexity: O(1)
            self.keys.insert(index, key)
            self.values.insert(index, [value])

        if len(self.keys) > self.order:                     # Time complexity: O(log n), Space complexity: O(1)
            self.split()

    def find_insert_index(self, key):                       # Time complexity: O(log n), Space complexity: O(1)
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1
        return index

    def split(self):                                       # Time complexity: O(log n), Space complexity: O(log n)
        mid = (len(self.keys) + 1) // 2
        new_node = BPlusNode(self.order)

        new_node.keys = self.keys[mid:]                    # Time complexity: O(log n), Space complexity: O(log n)
        new_node.values = self.values[mid:]                # Time complexity: O(log n), Space complexity: O(log n)
        new_node.children = self.children[mid:]            # Time complexity: O(log n), Space complexity: O(log n)
        new_node.is_leaf = self.is_leaf                    # Time complexity: O(1), Space complexity: O(1)
        new_node.next = self.next                          # Time complexity: O(1), Space complexity: O(1)

        self.keys = self.keys[:mid]                        # Time complexity: O(log n), Space complexity: O(log n)
        self.values = self.values[:mid]                    # Time complexity: O(log n), Space complexity: O(log n)
        self.children = self.children[:mid]                # Time complexity: O(log n), Space complexity: O(log n)
        self.next = new_node                                # Time complexity: O(1), Space complexity: O(1)

        parent = None
        if not self.is_leaf:
            parent = BPlusNode(self.order)
            parent.keys.append(new_node.keys[0])
            parent.children.append(new_node)
            parent.children.append(self)
            self.is_leaf = False

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
