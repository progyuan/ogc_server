'''Generic Graph Classes'''
import sys
from StringIO import StringIO
import cython
cimport cython
from cpython.version cimport PY_MAJOR_VERSION
import numpy as np
cimport numpy as np

cdef unicode _ustring(s):
    if type(s) is unicode:
        # fast path for most common case(s)
        return <unicode>s
    elif PY_MAJOR_VERSION < 3 and isinstance(s, bytes):
        # only accept byte strings in Python 2.x, not in Py3
        return (<bytes>s).decode('ascii')
    elif isinstance(s, unicode):
        # an evil cast to <unicode> might work here in some(!) cases,
        # depending on what the further processing does.  to be safe,
        # we can always create a copy instead
        return unicode(s)
    else:
        raise TypeError('unknown string type')

# @cython.boundscheck(False)
cdef class Node(object):

    # def __init__(self, name, parents=[], children=[]):
    #     self.name = name
    #     self.parents = parents[:]
    #     self.children = children[:]
    cdef char*  name
    cdef Node[:] parents = np.empty((100000,), dtype=Node)
    cdef Node[:] children = np.empty((100000,), dtype=Node)
    @cython.nonecheck(False)
    def __cinit__(self, char* name, Node[:] parents, Node[:] children):
        self.name = name
        self.parents = parents
        self.children = children

    def __repr__(self):
        return '<Node %s>' % self.name


cdef class UndirectedNode(object):

    # def __init__(self, name, neighbours=[]):
    #     self.name = name
    #     self.neighbours = neighbours[:]
    @cython.nonecheck(False)
    def __init__(self, name, neighbours=[]):
        self.name = name
        self.neighbours = neighbours[:]

    def __repr__(self):
        return '<UndirectedNode %s>' % self.name


class Graph(object):

    def export(self, filename=None, format='graphviz'):
        '''Export the graph in GraphViz dot language.'''
        if format != 'graphviz':
            raise 'Unsupported Export Format.'
        if filename:
            fh = open(filename, 'w')
        else:
            fh = sys.stdout
        fh.write(self.get_graphviz_source())

    def get_topological_sort(self):
        '''In order to make this sort
        deterministic we will use the
        variable name as a secondary sort'''
        l = []
        l_set = set() # For speed
        s = [n for n in self.nodes.values() if not n.parents]
        s.sort(reverse=True, key=lambda x:x.variable_name)
        while s:
            n = s.pop()
            l.append(n)
            l_set.add(n)
            # Now some of n's children may be
            # added to s if all their parents
            # are already accounted for.
            for m in n.children:
                if set(m.parents).issubset(l_set):
                    s.append(m)
                    s.sort(reverse=True, key=lambda x:x.variable_name)
        if len(l) == len(self.nodes):
            return l
        raise "Graph Has Cycles"


class UndirectedGraph(object):

    def __init__(self, nodes, name=None):
        self.nodes = nodes
        self.name = name

    def get_graphviz_source(self):
        fh = StringIO()
        fh.write('graph G {\n')
        fh.write('  graph [ dpi = 300 bgcolor="transparent" rankdir="LR"];\n')
        edges = set()
        for node in self.nodes:
            fh.write('  %s [ shape="ellipse" color="blue"];\n' % node.name)
            for neighbour in node.neighbours:
                edge = [node.name, neighbour.name]
                edges.add(tuple(sorted(edge)))
        for source, target in edges:
            fh.write('  %s -- %s;\n' % (source, target))
        fh.write('}\n')
        return fh.getvalue()

    def export(self, filename=None, format='graphviz'):
        '''Export the graph in GraphViz dot language.'''
        if format != 'graphviz':
            raise 'Unsupported Export Format.'
        if filename:
            fh = open(filename, 'w')
        else:
            fh = sys.stdout
        fh.write(self.get_graphviz_source())


def connect(parent, child):
    '''
    Make an edge between a parent
    node and a child node.
    a - parent
    b - child
    '''
    parent.children.append(child)
    child.parents.append(parent)
