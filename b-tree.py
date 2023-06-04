class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k[0] > x.keys[i][0]:
                    i += 1
            self.insert_non_full(x.child[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]

    def find(self, k):
        return self.find_in_node(self.root, k)

    def find_in_node(self, node, k):
        i = 0
        while i < len(node.keys) and k[0] > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and k[0] == node.keys[i][0]:
            return node.keys[i]
        elif node.leaf:
            return None
        else:
            return self.find_in_node(node.child[i], k)

    def range_search(self, start, end):
        result = []
        self.range_search_in_node(self.root, start, end, result)
        return result

    def range_search_in_node(self, node, start, end, result):
        i = 0
        while i < len(node.keys) and start[0] > node.keys[i][0]:
            i += 1
        if node.leaf:
            while i < len(node.keys) and start[0] <= node.keys[i][0] <= end[0]:
                result.append(node.keys[i])
                i += 1
        elif i < len(node.keys):
            self.range_search_in_node(node.child[i], start, end, result)
            if start[0] <= node.keys[i][0] <= end[0]:
                result.append(node.keys[i])
            if node.keys[i][0] < end[0]:
                self.range_search_in_node(node.child[i + 1], start, end, result)

    def remove(self, k):
        self.remove_from_node(self.root, k)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.child[0]

    def remove_from_node(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k[0] > node.keys[i][0]:
            i += 1
        if node.leaf:
            if i < len(node.keys) and node.keys[i][0] == k[0]:
                node.keys.pop(i)
        else:
            if i < len(node.keys) and node.keys[i][0] == k[0]:
                return self.remove_internal_node(node, k, i)
            elif len(node.child[i].keys) >= t:
                self.remove_from_node(node.child[i], k)
            else:
                if i != 0 and i + 2 < len(node.child):
                    if len(node.child[i - 1].keys) >= t:
                        self.remove_sibling(node, i, i - 1)
                    elif len(node.child[i + 1].keys) >= t:
                        self.remove_sibling(node, i, i + 1)
                    else:
                        self.remove_merge(node, i, i + 1)
                elif i == 0:
                    if len(node.child[i + 1].keys) >= t:
                        self.remove_sibling(node, i, i + 1)
                    else:
                        self.remove_merge(node, i, i + 1)
                elif i + 1 == len(node.child):
                    if len(node.child[i - 1].keys) >= t:
                        self.remove_sibling(node, i, i - 1)
                    else:
                        self.remove_merge(node, i, i - 1)
                self.remove_from_node(node.child[i], k)

    def remove_internal_node(self, x, k, i):
        t = self.t
        if x.leaf:
            if x.keys[i][0] == k[0]:
                x.keys.pop(i)
        else:
            if len(x.child[i].keys) >= t:
                x.keys[i] = self.remove_predecessor(x.child[i])
            elif len(x.child[i + 1].keys) >= t:
                x.keys[i] = self.remove_successor(x.child[i + 1])
            else:
                self.remove_merge(x, i, i + 1)
                self.remove_internal_node(x.child[i], k, t - 1)

    def remove_predecessor(self, x):
        if x.leaf:
            return x.keys.pop()
        n = len(x.keys) - 1
        if len(x.child[n].keys) >= self.t:
            self.remove_sibling(x, n + 1, n)
        else:
            self.remove_merge(x, n, n + 1)
        return self.remove_predecessor(x.child[n])

    def remove_successor(self, x):
        if x.leaf:
            return x.keys.pop(0)
        if len(x.child[1].keys) >= self.t:
            self.remove_sibling(x, 0, 1)
        else:
            self.remove_merge(x, 0, 1)
        return self.remove_successor(x.child[0])

    def remove_merge(self, x, i, j):
        cnode = x.child[i]
        if j > i:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.child) > 0:
                    cnode.child.append(rsnode.child[k])
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop())
            new_key = x.keys.pop(i)
            rsnode.keys = []
            rsnode.child = []
        else:
            lsnode = x.child[j]
            lsnode.keys.append(x.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(lsnode.child) > 0:
                    lsnode.child.append(cnode.child[i])
            if len(lsnode.child) > 0:
                lsnode.child.append(cnode.child.pop())
            new_key = x.keys.pop(j)
            cnode.keys = []
            cnode.child = []
        if x == self.root and len(x.keys) == 0:
            self.root = cnode

    def remove_sibling(self, x, i, j):
        cnode = x.child[i]
        if i < j:
            rsnode = x.child[j]
            cnode.keys.append(x.keys[i])
            new_key = rsnode.keys.pop(0)
            x.keys[i] = new_key
            if len(rsnode.child) > 0:
                cnode.child.append(rsnode.child.pop(0))
        else:
            lsnode = x.child[j]
            cnode.keys.insert(0, x.keys[i - 1])
            new_key = lsnode.keys.pop()
            x.keys[i - 1] = new_key
            if len(lsnode.child) > 0:
                cnode.child.insert(0, lsnode.child.pop())

    def __iter__(self):
        yield from self.traverse(self.root)

    def traverse(self, x):
        i = 0
        while i < len(x.keys):
            if x.leaf:
                yield x.keys[i]
            else:
                yield from self.traverse(x.child[i])
                yield x.keys[i]
            i += 1
        if not x.leaf:
            yield from self.traverse(x.child[i])

    def print_tree(self):
        self.print_node(self.root)

    def print_node(self, x):
        for i in x.keys:
            print(i, end=" ")
        print()
        if not x.leaf:
            for i in x.child:
                self.print_node(i)


B = BTree(3)

B.insert((1, 2))
B.insert((3, 6))
B.insert((4, 8))
B.insert((5, 10))
B.insert((6, 12))
B.insert((7, 14))
B.insert((8, 16))
B.insert((9, 18))

B.print_tree()

print()

print(B.find((5, 10)))

print()

print(B.range_search((3, 6), (7, 14)))

print()

B.remove((5, 10))

B.print_tree()
