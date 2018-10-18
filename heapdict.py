import collections


def doc(s):
    if hasattr(s, '__call__'):
        s = s.__doc__

    def f(g):
        g.__doc__ = s
        return g

    return f


def _set(arr, i, item):
    arr[i] = item
    item[2] = i


def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    item[2] = len(heap)
    heap.append(item)
    _siftdown(heap, item[2])


def heappop(heap, i=0):
    """Pop an item off the heap, maintaining the heap invariant."""
    returnitem = heap[i]  # raises appropriate IndexError if invalid index.
    lastelt = heap.pop()
    # If we are not returning the last node, put it at i and sift it into place.
    if lastelt is not returnitem:
        _set(heap, i, lastelt)
        # if lastelt is greater than the previous node, move it down.
        if lastelt[0] > returnitem[0]:
            _siftup(heap, i)
        # otherwise it must be equal or smaller, move it up.
        else:
            _siftdown(heap, i)
    return returnitem


def heapify(heap):
    """Transform list into a heap, in-place, in O(len(heap)) time."""
    # Transform bottom-up.  The largest index there's any point to looking at
    # is the largest with a child index in-range, so must have 2*i + 1 < n,
    # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
    # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
    # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
    for i in reversed(xrange(len(heap)//2)):
        _siftup(heap, i)


# 'heap' is a heap at all indices < pos. 'pos' is the index of a node that may
# need to be moved up. Shift the node at pos up to restore the heap invariant.
def _siftdown(heap, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > 0:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem[0] >= parent[0]:
            break
        _set(heap, pos, parent)
        pos = parentpos
    _set(heap, pos, newitem)

# 'heap' is a heap at all indicies > pos. 'pos' is the index of a node that may
# need to be moved down. Shift the entry at pos down to restore the heap invariant.
def _siftup(heap, pos):
    endpos = len(heap)
    newitem = heap[pos]
    # Bubble up the smaller child until we find the right position.
    childpos = 2 * pos + 1  # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and heap[childpos][0] > heap[rightpos][0]:
            childpos = rightpos
        child = heap[childpos]
        if newitem[0] <= child[0]:
            break
        # Move the smaller child up.
        _set(heap, pos, child)
        pos = childpos
        childpos = 2 * pos + 1
    # The node at pos is empty now, put newitem there.
    _set(heap, pos, newitem)


class heapdict(collections.MutableMapping):

    def _check_invariants(self):
        # the 3rd entry of each heap entry is the position in the heap
        for i, e in enumerate(self.heap):
            assert e[2] == i
        # the parent of each heap element must not be larger than the element
        for i in range(1, len(self.heap)):
            parent = (i - 1) >> 1
            assert self.heap[parent][0] <= self.heap[i][0]

    def __init__(self, *args, **kw):
        self.d = dict(*args, **kw)
        self.heap = [[v, k, i] for (i, (k, v)) in enumerate(self.d.iteritems())]
        self.d.update((e[1], e) for e in self.heap)
        heapify(self.heap)

    @doc(dict.clear)
    def clear(self):
        del self.heap[:]
        self.d.clear()

    @doc(dict.__setitem__)
    def __setitem__(self, key, value):
        if key in self.d:
            wrapper = self.d[key]
            oldvalue, _, i = wrapper
            wrapper[0] = value
            if oldvalue < value:
                _siftup(self.heap, i)
            else:
                _siftdown(self.heap, i)
        else:
            wrapper = [value, key, -2]
            self.d[key] = wrapper
            heappush(self.heap, wrapper)

    @doc(dict.__delitem__)
    def __delitem__(self, key):
        i = self.d[key][2]
        heappop(self.heap, i)
        del self.d[key]

    @doc(dict.__getitem__)
    def __getitem__(self, key):
        return self.d[key][0]

    @doc(dict.__iter__)
    def __iter__(self):
        return iter(self.d)

    @doc(dict.__len__)
    def __len__(self):
        return len(self.d)

    def pop(self, *args):
        """D.pop([k,[,d]]) -> v, if no key is specified, remove the key with the lowest
value and return the corresponding value, raising IndexError if list is empty.
If a key is specified, then it is removed instead if present and the
corresponding value is returned. If the key is specified and not present, then
d is returned if given, otherwise KeyError is raised"""
        if len(args) == 0:
            return self.popitem()[0]
        else:
            return super(heapdict, self).pop(*args)

    def popitem(self):
        """D.popitem() -> (k, v), remove and return the (key, value) pair with lowest\nvalue; but raise KeyError if D is empty."""
        wrapper = heappop(self.heap)
        del self.d[wrapper[1]]
        return (wrapper[1], wrapper[0])

    def peekitem(self):
        """D.peekitem() -> (k, v), return the (key, value) pair with lowest value;\n but raise KeyError if D is empty."""
        wrapper = self.heap[0]
        return (wrapper[1], wrapper[0])


del doc
__all__ = ['heapdict']
