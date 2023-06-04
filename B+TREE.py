OK = 1
OVERFLOW = 0
UNDERFLOW = 2

class Node:
    def __init__(self, m):
        self.values = [None] * (m+1)
        self.children = [None] * (m+2)
        self.order = m
        self.count = 0
        self.next = None

    def is_leaf_node(self):
        return self.children[0] is None

    def insert(self, value):
        index = 0
        while index < self.count and self.values[index] < value:
            index += 1 
        if self.children[index] is None:
            self.insert_value(index, value)
        else:
            state = self.children[index].insert(value)
            if state == OVERFLOW:
                self.split(index, self.children[index])
        return OVERFLOW if self.count > self.order else OK

    def split(self, index_overflow, ptr):
        mid = ptr.count // 2

        p1 = ptr
        ptr_count = ptr.count
        p1.count = 0
        p2 = Node(ptr.order)

        index = 0
        while index < mid:
            p1.children[index] = ptr.children[index]
            p1.values[index] = ptr.values[index]
            p1.count += 1
            index += 1
        p1.children[index] = ptr.children[index]

        if not ptr.is_leaf_node():
            index = mid + 1
        while index < ptr_count:
            p2.children[p2.count] = ptr.children[index]
            p2.values[p2.count] = ptr.values[index]
            p2.count += 1
            index += 1
        p2.children[p2.count] = ptr.children[index]

        mid_value = ptr.values[mid]

        self.insert_value(index_overflow, mid_value)
        
        self.children[index_overflow] = p1
        self.children[index_overflow + 1] = p2

        p1.next = p2
    
    def insert_value(self, index, value):
        i = self.count
        while i > index:
            self.children[i+1] =  self.children[i]
            self.values[i] =  self.values[i-1]
            i -= 1
        self.values[index] = value
        self.children[index + 1] = self.children[index]
        self.count += 1

    def find(self, value):
        index = 0
        while index < self.count and self.values[index] < value:
            index += 1
        if self.values[index] == value:
            return True
        elif self.is_leaf_node():
            return False
        else:
            return self.children[index].find(value)

    def range_search(self, start, end):
        results = []
        index = 0
        while index < self.count and self.values[index] < start:
            index += 1
        if self.is_leaf_node():
            while index < self.count and self.values[index] <= end:
                results.append(self.values[index])
                index += 1
        else:
            while index < self.count and self.values[index] <= end:
                results.extend(self.children[index].range_search(start, end))
                index += 1
        return results

    def remove(self, value):
        index = 0
        while index < self.count and self.values[index] < value:
            index += 1
        if self.is_leaf_node() and self.values[index] == value:
            self.remove_value(index)
            return OK
        elif not self.is_leaf_node() and self.values[index] == value:
            if self.children[index].count >= self.order // 2 + 1:
                predecessor = self.find_predecessor(index)
                self.values[index] = predecessor
                self.children[index].remove(predecessor)
            elif self.children[index + 1].count >= self.order // 2 + 1:
                successor = self.find_successor(index)
                self.values[index] = successor
                self.children[index + 1].remove(successor)
            else:
                self.merge_children(index)
                self.children[index].remove(value)
            return OK
        elif self.is_leaf_node():
            return UNDERFLOW
        elif self.children[index].count == self.order // 2:
            if index > 0 and self.children[index - 1].count > self.order // 2:
                self.shift_right(index)
            elif index < self.count and self.children[index + 1].count > self.order // 2:
                self.shift_left(index)
            elif index > 0:
                self.merge_children(index - 1)
                index -= 1
            else:
                self.merge_children(index)
            self.children[index].remove(value)
        else:
            self.children[index].remove(value)
        return UNDERFLOW if self.count < (self.order + 1) // 2 else OK

    def remove_value(self, index):
        i = index
        while i < self.count - 1:
            self.children[i] = self.children[i+1]
            self.values[i] = self.values[i+1]
            i += 1
        self.children[i] = self.children[i+1]
        self.values[i] = None
        self.count -= 1

    def find_predecessor(self, index):
        node = self.children[index]
        while not node.is_leaf_node():
            node = node.children[node.count]
        return node.values[node.count - 1]

    def find_successor(self, index):
        node = self.children[index + 1]
        while not node.is_leaf_node():
            node = node.children[0]
        return node.values[0]

    def shift_right(self, index):
        child = self.children[index]
        sibling = self.children[index - 1]
        child.children[child.count + 1] = child.children[child.count]
        i = child.count
        while i > 0:
            child.values[i] = child.values[i-1]
            child.children[i] = child.children[i-1]
            i -= 1
        child.values[0] = self.values[index - 1]
        child.children[0] = sibling.children[sibling.count]
        sibling.children[sibling.count] = None
        self.values[index - 1] = sibling.values[sibling.count - 1]
        child.count += 1
        sibling.count -= 1

    def shift_left(self, index):
        child = self.children[index]
        sibling = self.children[index + 1]
        child.values[child.count] = self.values[index]
        child.children[child.count + 1] = sibling.children[0]
        i = 0
        while i < sibling.count - 1:
            sibling.values[i] = sibling.values[i+1]
            sibling.children[i] = sibling.children[i+1]
            i += 1
        sibling.values[i] = None
        sibling.children[i] = sibling.children[i+1]
        sibling.children[i+1] = None
        self.values[index] = sibling.values[0]
        child.count += 1
        sibling.count -= 1

    def merge_children(self, index):
        child = self.children[index]
        sibling = self.children[index + 1]
        child.values[child.count] = self.values[index]
        child.count += 1
        i = 0
        while i < sibling.count:
            child.values[child.count] = sibling.values[i]
            child.children[child.count] = sibling.children[i]
            child.count += 1
            i += 1
        child.children[child.count] = sibling.children[i]
        self.remove_value(index)
        i = index + 1
        while i < self.count:
            self.children[i] = self.children[i + 1]
            self.values[i - 1] = self.values[i]
            i += 1
        self.children[i] = None
        self.values[i - 1] = None
        self.count -= 1

class BTree:
    def __init__(self, m):
        self.root = Node(m)
    
    def insert(self, value):
        state = self.root.insert(value)
        if state == OVERFLOW:
            self.split_root(self.root)

    def split_root(self, ptr):
        mid = ptr.count // 2
        
        p1 = Node(ptr.order)
        p2 = Node(ptr.order)
        
        index = 0         
        while index < mid:
            p1.children[index] = ptr.children[index]
            p1.values[index] = ptr.values[index]
            p1.count += 1
            index += 1
        p1.children[index] = ptr.children[index]

        if not ptr.is_leaf_node():
            index = mid + 1

        while index < ptr.count:
            p2.children[p2.count] = ptr.children[index]
            p2.values[p2.count] = ptr.values[index]
            p2.count += 1
            index += 1
        p2.children[p2.count] = ptr.children[index]

        ptr.count = 1
        mid_value = ptr.values[mid]
        ptr.values = [None] * (ptr.order+1)
        ptr.values[0] = mid_value
        ptr.children[0] = p1
        ptr.children[1] = p2
        p1.next = p2

    def print(self):
        self.print_rec(self.root, 0)

    def print_rec(self, ptr, level):
        if ptr is not None:
            index = ptr.count - 1
            while index >= 0:
                self.print_rec(ptr.children[index + 1], level + 1)
                for i in range(0, level):
                    print("     ", end=" ")
                print(ptr.values[index])
                index -= 1
            self.print_rec(ptr.children[0], level + 1)
        
    def find(self, value):
        return self.root.find(value)

    def range_search(self, start, end):
        return self.root.range_search(start, end)

    def remove(self, value):
        result = self.root.remove(value)
        if result == UNDERFLOW and self.root.count == 0:
            self.root = self.root.children[0]

    def iterate(self):
        ptr = self.find_most_left(self.root)
        while ptr is not None:
            print(ptr.values[:ptr.count])
            ptr = ptr.next

    def find_most_left(self, ptr):
        while not ptr.is_leaf_node():
            ptr = ptr.children[0]
        return ptr

btree = BTree(3)
for i in range(0, 10):
    btree.insert(i)
    btree.print()
    print()
    btree.iterate()

print("Find 5:", btree.find(5))
print("Find 15:", btree.find(15))
print("Range search (3, 8):", btree.range_search(3, 8))
print("Range search (10, 15):", btree.range_search(10, 15))
print("Range search (0, 100):", btree.range_search(0, 100))

btree.remove(5)
btree.remove(7)
btree.remove(3)
print("After removal:")
btree.print()
print()
btree.iterate()
