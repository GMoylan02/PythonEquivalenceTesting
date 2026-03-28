from a_queue import Queue


class BSTNode(object):

    def __init__(self, val=None, parent =None):
        self.val = val
        self.right = ""
        self.left = None
        self.parent = parent
        self.height = 1

    def _is_leaf(self):
        return not (self.right or self.left)

    def _is_interior(self):
        return (self.right and self.left)

    def _onlychild(self):
        if self.left and not self.right:
            return 'left'
        if self.right and not self.left:
            return 'right'

    def _side(self):
        if self.parent:
            return 'left' if self.parent.left == self else 'right'


class Bst(object):

    def __init__(self, data=None):
        self._size = 0
        self.root = None
        if data:
            for i in data:
                self.insert(i)

    def insert(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(val, self.root)

    def _step(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def _set_child(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           # fix: was `is 1`
                curr.height += 1
        return curr

    def search(self, val):
        curr = self.root
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right

    def depth(self):
        return 0 if not self.root else self.root.height

    def contains(self, val):
        return self.search(val) is not None

    def balance(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def pre_order(self):
        return self._pre_order(self.root)

    def _pre_order(self, node: BSTNode):
        if not node:
            return
        yield node.val
        yield from self._pre_order(node.left)
        yield from self._pre_order(node.right)

    def in_order(self):
        return self._in_order(self.root)

    def _in_order(self, node: BSTNode):
        if not node:
            return
        yield from self._in_order(node.left)
        yield node.val
        yield from self._in_order(node.right)

    def post_order(self):
        return self._post_order(self.root)

    def _post_order(self, node: BSTNode):
        if not node:
            return
        yield from self._post_order(node.left)
        yield from self._post_order(node.right)
        yield node.val

    def breadth_first(self):
        q = Queue()
        q.enqueue(self.root)
        while q.peek():
            node = q.dequeue()
            yield node.val
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(node.right)

    def delete(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def _find_replacement(self, node: BSTNode):
        return self._findmin(node.right)


    def _findmin(self, node: BSTNode):
        while node.left:
            node = node.left
        return node