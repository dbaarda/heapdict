import collections


def doc(s):
    if hasattr(s, '__call__'):
        s = s.__doc__

    def f(g):
        g.__doc__ = s
        return g

    return f


def _swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arr[i][2] = i
    arr[j][2] = j


def _set(arr, i, item):
    arr[i] = item
    item[2] = i


def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    item[2] = len(heap)
    heap.append(item)
    _siftdown(heap, 0, len(heap) - 1)


def heappop(heap):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()  # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        _set(heap, 0, lastelt)
        _siftup(heap, 0)
        return returnitem
    return lastelt


# 'heap' is a heap at all indices >= startpos, except possibly for pos.  pos
# is the index of a leaf with a possibly out-of-order value.  Restore the
# heap invariant.
def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem[0] < parent[0]:
            _set(heap, pos, parent)
            pos = parentpos
            continue
        break
    _set(heap, pos, newitem)


def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2 * pos + 1  # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos][0] < heap[rightpos][0]:
            childpos = rightpos
        # Move the smaller child up.
        _set(heap, pos, heap[childpos])
        pos = childpos
        childpos = 2 * pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    _set(heap, pos, newitem)
    _siftdown(heap, startpos, pos)


class heapdict(collections.MutableMapping):
    __marker = object()

    def _check_invariants(self):
        # the 3rd entry of each heap entry is the position in the heap
        for i, e in enumerate(self.heap):
            assert e[2] == i
        # the parent of each heap element must not be larger than the element
        for i in range(1, len(self.heap)):
            parent = (i - 1) >> 1
            assert self.heap[parent][0] <= self.heap[i][0]

    def __init__(self, *args, **kw):
        self.heap = []
        self.d = {}
        self.update(*args, **kw)

    @doc(dict.clear)
    def clear(self):
        del self.heap[:]
        self.d.clear()

    @doc(dict.__setitem__)
    def __setitem__(self, key, value):
        if key in self.d:
            del self[key]
        wrapper = [value, key, -2]
        self.d[key] = wrapper
        heappush(self.heap, wrapper)

    @doc(dict.__delitem__)
    def __delitem__(self, key):
        wrapper = self.d[key]
        i = wrapper[2]
        lastindex = len(self.heap) - 1
        # swap with last item
        _swap(self.heap, i, lastindex)
        self.heap.pop()
        if self.heap and i < lastindex:
            _siftup(self.heap, i)
            _siftdown(self.heap, 0, i)
        del self.d[key]

    @doc(dict.__getitem__)
    def __getitem__(self, key):
        return self.d[key][0]

    @doc(dict.__iter__)
    def __iter__(self):
        return iter(self.d)

    def pop(self, *args):
        """D.pop([k,[,d]]) -> v, if no key is specified, remove the key with the lowest
value and return the corresponding value, raising IndexError if list is empty.
If a key is specified, then it is removed instead if present and the
corresponding value is returned. If the key is specified and not present, then
d is returned if given, otherwise KeyError is raised"""
        if len(args) == 0:
            if len(self.d) == 0:
                raise IndexError("pop from empty heapdict")
            (k, _) = self.popitem()
        else:
            k = super(heapdict, self).pop(*args)
        return k

    def popitem(self):
        """D.popitem() -> (k, v), remove and return the (key, value) pair with lowest\nvalue; but raise KeyError if D is empty."""
        wrapper = heappop(self.heap)
        del self.d[wrapper[1]]
        return wrapper[1], wrapper[0]

    @doc(dict.__len__)
    def __len__(self):
        return len(self.d)

    def peekitem(self):
        """D.peekitem() -> (k, v), return the (key, value) pair with lowest value;\n but raise KeyError if D is empty."""
        return (self.heap[0][1], self.heap[0][0])


del doc
__all__ = ['heapdict']
