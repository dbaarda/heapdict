#!/usr/bin/python
from __future__ import print_function
from heapdict import heapdict
import random
import unittest
import sys
try:
    # Python 3
    import test.support as test_support
except ImportError:
    # Python 2
    import test.test_support as test_support

N = 100


class TestHeap(unittest.TestCase):

    def make_data(self):
        pairs = [(random.random(), random.random()) for i in range(N)]
        h = heapdict()
        d = {}
        for k, v in pairs:
            h[k] = v
            d[k] = v

        pairs.sort(key=lambda x: x[1], reverse=True)
        return h, pairs, d

    def test_pop(self):
        # verify that we raise IndexError on empty heapdict
        empty_heap = heapdict()
        self.assertRaises(IndexError, empty_heap.pop)
        # test adding a bunch of random values at random priorities
        h, pairs, d = self.make_data()
        last_priority = 0
        while pairs:
            v1 = h.pop()
            (v2, priority) = pairs.pop()
            # confirm that our heapdict is returning things in sorted order
            self.assertEqual(v1, v2)
            # verify that our items are increasing in priority value
            self.assertGreater(priority, last_priority)
            last_priority = priority
        # make sure that we got everything out of the heap
        self.assertEqual(len(h), 0)
        # now verify that we raise KeyError if we try to remove something
        # by key that is not present
        empty_heap = heapdict()
        self.assertRaises(KeyError, empty_heap.pop, "missing")
        # verify that we do *not* get a KeyError if we specify a default
        empty_heap = heapdict()
        self.assertEqual(empty_heap.pop("missing", 123), 123)
        # confirm that we can get a value by key if it is present
        h = heapdict()
        h["foo"] = 10
        self.assertEqual(len(h), 1)
        self.assertEqual(h.pop("foo"), 10)
        self.assertEqual(len(h), 0)
        # verify that removing keys does the right thing to a heap
        h = heapdict()
        h["c"] = 30
        h["a"] = 10
        h["b"] = 20
        self.assertEqual(len(h), 3)
        self.assertEqual(h.pop("b"), 20)
        self.assertEqual(h.pop(), "a")
        self.assertEqual(h.pop(), "c")
        self.assertEqual(len(h), 0)

    def test_popitem(self):
        h, pairs, d = self.make_data()
        while pairs:
            v = h.popitem()
            v2 = pairs.pop()
            self.assertEqual(v, v2)
        self.assertEqual(len(h), 0)

    def test_popitem_ties(self):
        h = heapdict()
        for i in range(N):
            h[i] = 0
        for i in range(N):
            k, v = h.popitem()
            self.assertEqual(v, 0)
            h._check_invariants()

    def test_peek(self):
        h, pairs, d = self.make_data()
        while pairs:
            v = h.peekitem()[0]
            h.popitem()
            v2 = pairs.pop()
            self.assertEqual(v, v2[0])
        self.assertEqual(len(h), 0)

    def test_iter(self):
        h, pairs, d = self.make_data()
        self.assertEqual(list(h), list(d))

    def test_keys(self):
        h, pairs, d = self.make_data()
        self.assertEqual(list(sorted(h.keys())), list(sorted(d.keys())))

    def test_values(self):
        h, pairs, d = self.make_data()
        self.assertEqual(list(sorted(h.values())), list(sorted(d.values())))

    def test_del(self):
        h, pairs, d = self.make_data()
        k, v = pairs.pop(N//2)
        del h[k]
        while pairs:
            v = h.popitem()
            v2 = pairs.pop()
            self.assertEqual(v, v2)
        self.assertEqual(len(h), 0)

    def test_change(self):
        h, pairs, d = self.make_data()
        k, v = pairs[N//2]
        h[k] = 0.5
        pairs[N//2] = (k, 0.5)
        pairs.sort(key=lambda x: x[1], reverse=True)
        while pairs:
            v = h.popitem()
            v2 = pairs.pop()
            self.assertEqual(v, v2)
        self.assertEqual(len(h), 0)

    def test_clear(self):
        h, pairs, d = self.make_data()
        h.clear()
        self.assertEqual(len(h), 0)


def test_main(verbose=None):
    test_classes = [TestHeap]
    test_support.run_unittest(*test_classes)

    # verify reference counting
    if verbose and hasattr(sys, "gettotalrefcount"):
        import gc
        counts = [None] * 5
        for i in range(len(counts)):
            test_support.run_unittest(*test_classes)
            gc.collect()
            counts[i] = sys.gettotalrefcount()
        print(counts)


if __name__ == "__main__":
    test_main(verbose=True)
