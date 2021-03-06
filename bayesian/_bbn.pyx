from __future__ import division
'''Data Structures to represent a BBN as a DAG.'''
import sys, time
import copy
import heapq
import inspect
cimport cython
import cython
from cpython cimport bool

from random import random, choice
from StringIO import StringIO
from itertools import combinations, product
from collections import defaultdict

from prettytable import PrettyTable

from bayesian import GREEN, NORMAL
# from bayesian.graph import Node, UndirectedNode, connect
# from bayesian.graph import Graph, UndirectedGraph
# from bayesian.utils import get_args, named_base_type_factory
# from bayesian.utils import get_original_factors
# from bayesian._graph import Node, UndirectedNode, connect
# from bayesian._graph import Graph, UndirectedGraph
# from bayesian.utils import get_original_factors




cdef class Node(object):
    cdef str name
    cdef list parents
    cdef list children
    def __cinit__(self, str name, list parents=[], list children=[]):
        self.name = name
        self.parents = parents[:]
        self.children = children[:]
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name ):
            self.name = name
    property parents:
        def __get__(self):
            return self.parents
        def __set__(self, list parents):
            self.parents = parents
    property children:
        def __get__(self):
            return self.children
        def __set__(self, list children):
            self.children = children

    def __repr__(self):
        return '<Node %s>' % self.name


cdef class UndirectedNode(object):
    cdef str name
    cdef list neighbours
    cdef object func
    cdef str variable_name
    cdef list argspec

    def __cinit__(self, str name, list neighbours=[]):
        self.name = name
        self.neighbours = neighbours[:]
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name ):
            self.name = name
    property neighbours:
        def __get__(self):
            return self.neighbours
        def __set__(self, list neighbours):
            self.neighbours = neighbours
    property func:
        def __get__(self):
            return self.func
        def __set__(self, object func):
            self.func = func
    property argspec:
        def __get__(self):
            return self.argspec
        def __set__(self, list argspec):
            self.argspec = argspec
    property variable_name:
        def __get__(self):
            return self.variable_name
        def __set__(self, str variable_name ):
            self.variable_name = variable_name

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls, self.name, self.neighbours)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls, self.name, self.neighbours)
        memo[id(self)] = result
        # for k, v in self.__dict__.items():
        for k, v in [('name', self.name),
                     ('neighbours', self.neighbours),
                     ('variable_name', self.variable_name),
                     ('argspec', self.argspec),
                     ('func', self.func),
                     ]:
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __repr__(self):
        return '<UndirectedNode %s>' % self.name


cdef class Graph(object):

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


cdef class UndirectedGraph(object):
    cdef str name
    cdef list nodes
    property nodes:
        def __get__(self):
            return self.nodes
        def __set__(self, list nodes):
            self.nodes = nodes
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name):
            self.name = name

    def __cinit__(self, list nodes, str name=None):
        self.nodes = nodes
        self.name = name
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls, self.nodes, self.name)
        memo[id(self)] = result
        # for k, v in self.__dict__.items():
        for k, v in [('name', self.name),('nodes', self.nodes)]:
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def get_graphviz_source(self, dpi=200, rankdir='LL'):
        fh = StringIO()
        fh.write('graph G {\n')
        fh.write('  graph [ dpi = %d bgcolor="transparent" rankdir="%s"];\n' % (dpi, rankdir))
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


cdef connect(BBNNode parent, BBNNode child):
    '''
    Make an edge between a parent
    node and a child node.
    a - parent
    b - child
    '''
    parent.children.append(child)
    child.parents.append(parent)


cdef list get_args(object func):
    '''
    Return the names of the arguments
    of a function as a list of strings.
    This is so that we can omit certain
    variables when we marginalize.
    Note that functions created by
    make_product_func do not return
    an argspec, so we add a argspec
    attribute at creation time.
    '''
    if hasattr(func, 'argspec'):
        return func.argspec
    return inspect.getargspec(func).args


cdef class BBNNode(object):
    cdef str name
    cdef str variable_name
    cdef list parents
    cdef list children
    cdef object func
    cdef list argspec
    cdef JoinTreeCliqueNode clique
    property argspec:
        def __get__(self):
            return self.argspec
        def __set__(self, list argspec):
            self.argspec = argspec
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name ):
            self.name = name
    property variable_name:
        def __get__(self):
            return self.variable_name
        def __set__(self, str variable_name ):
            self.variable_name = variable_name
    property parents:
        def __get__(self):
            return self.parents
        def __set__(self, list parents):
            self.parents = parents
    property children:
        def __get__(self):
            return self.children
        def __set__(self, list children):
            self.children = children
    property func:
        def __get__(self):
            return self.func
        def __set__(self, object func):
            self.func = func
    property clique:
        def __get__(self):
            return self.clique
        def __set__(self, JoinTreeCliqueNode clique):
            self.clique = clique

    def __cinit__(self, str name, object factor, list parents=[], list children=[]):
        self.name = name
        self.func = factor
        self.argspec = get_args(factor)
        self.parents = parents[:]
        self.children = children[:]

    def __repr__(self):
        return '<BBNNode %s (%s)>' % (
            self.name,
            str(self.argspec))



cdef class BBN(object):
    '''A Directed Acyclic Graph'''
    cdef list nodes
    cdef dict vars_to_nodes
    cdef str name
    cdef dict domains
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name):
            self.name = name
    property domains:
        def __get__(self):
            return self.domains
        def __set__(self, dict domains):
            self.domains = domains
    property vars_to_nodes:
        def __get__(self):
            return self.vars_to_nodes
        def __set__(self, dict vars_to_nodes):
            self.vars_to_nodes = vars_to_nodes
    property nodes:
        def __get__(self):
            return self.nodes
        def __set__(self, list nodes):
            self.nodes = nodes

    def __cinit__(self, dict nodes_dict, str name=None, dict domains={}):
        self.nodes = nodes_dict.values()
        self.vars_to_nodes = nodes_dict
        self.domains = domains
        # For each node we want
        # to explicitly record which
        # variable it 'introduced'.
        # Note that we cannot record
        # this duing Node instantiation
        # becuase at that point we do
        # not yet know *which* of the
        # variables in the argument
        # list is the one being modeled
        # by the function. (Unless there
        # is only one argument)
        for variable_name, node in nodes_dict.items():
            if isinstance(variable_name, unicode):
                variable_name = variable_name.encode('utf-8')
            node.variable_name = variable_name

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



    def get_graphviz_source(self, dpi=200, rankdir='LL'):
        fh = StringIO()
        fh.write('digraph G {\n')
        fh.write('  graph [ dpi = %d bgcolor="transparent" rankdir="%s"];\n' % (dpi, rankdir))
        edges = set()
        for node in sorted(self.nodes, key=lambda x: x.name):
            fh.write('  %s [ shape="ellipse" color="blue"];\n' % node.name)
            for child in node.children:
                edge = (node.name, child.name)
                edges.add(edge)
        for source, target in sorted(edges, key=lambda x: (x[0], x[1])):
            fh.write('  %s -> %s;\n' % (source, target))
        fh.write('}\n')
        return fh.getvalue()

    def build_join_tree(self):
        jt = build_join_tree(self)
        return jt

    def query(self, **kwds):
        return self._query(kwds)
    # @cython.boundscheck(False)
    # @cython.wraparound(False)
    cdef dict _query(self, dict kwds):
        cdef JoinTree jt = self.build_join_tree()
        cdef dict assignments = jt.assign_clusters(self)
        cdef dict marginals
        jt.initialize_potentials(assignments, self, kwds)
        # print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'after initialize_potentials'))
        jt.propagate()
        marginals = dict()
        normalizers = defaultdict(float)
        for node in self.nodes:
            for k, v in jt.marginal(node).items():
                # For a single node the
                # key for the marginal tt always
                # has just one argument so we
                # will unpack it here
                marginals[k[0]] = v
                # If we had any evidence then we
                # need to normalize all the variables
                # not evidenced.
                if kwds:
                    normalizers[k[0][0]] += v
        # print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'after phase2'))

        if kwds:
            for k, v in marginals.iteritems():
                if normalizers[k[0]] != 0:
                    marginals[k] /= normalizers[k[0]]
        return marginals

    def q(self, **kwds):
        '''Interactive user friendly wrapper
        around query()
        '''
        result = self.query(**kwds)
        tab = PrettyTable(['Node', 'Value', 'Marginal'], sortby='Node')
        tab.align = 'l'
        tab.align['Marginal'] = 'r'
        tab.float_format = '%8.6f'
        for (node, value), prob in result.items():
            if kwds.get(node, '') == value:
                tab.add_row(['%s*' % node,
                             '%s%s*%s' % (GREEN, value, NORMAL),
                             '%8.6f' % prob])
            else:
                tab.add_row([node, value, '%8.6f' % prob])
        print tab

    def draw_samples(self, query={}, n=1):
        '''query is a dict of currently evidenced
        variables and is none by default.'''
        samples = []
        result_cache = dict()
        # We need to add evidence variables to the sample...
        while len(samples) < n:
            sample = dict(query)
            while len(sample) < len(self.nodes):
                next_node = choice([node for node in
                                    self.nodes if
                                    node.variable_name not in sample])
                key = tuple(sorted(sample.items()))
                if key not in result_cache:
                    # result_cache[key] = self.query(**sample)
                    result_cache[key] = self.query(sample)
                result = result_cache[key]
                var_density = [r for r in result.items()
                               if r[0][0]==next_node.variable_name]
                cumulative_density = var_density[:1]
                for key, mass in var_density[1:]:
                    cumulative_density.append((key, cumulative_density[-1][1] + mass))
                r = random()
                i = 0
                while r > cumulative_density[i][1]:
                    i += 1
                sample[next_node.variable_name] = cumulative_density[i][0][1]
            samples.append(sample)
        return samples


cdef class JoinTree(object):
    cdef str name
    cdef list nodes
    property nodes:
        def __get__(self):
            return self.nodes
        def __set__(self, list nodes):
            self.nodes = nodes
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name):
            self.name = name

    def __cinit__(self, list nodes, str name=None):
        self.nodes = nodes
        self.name = name


    def export(self, filename=None, format='graphviz'):
        '''Export the graph in GraphViz dot language.'''
        if format != 'graphviz':
            raise 'Unsupported Export Format.'
        if filename:
            fh = open(filename, 'w')
        else:
            fh = sys.stdout
        fh.write(self.get_graphviz_source())

    property sepset_nodes:
        def __get__(self):
            return [n for n in self.nodes if isinstance(n, JoinTreeSepSetNode)]
    # @property
    # def sepset_nodes(self):
    #     return [n for n in self.nodes if isinstance(n, JoinTreeSepSetNode)]

    property clique_nodes:
        def __get__(self):
            return [n for n in self.nodes if isinstance(n, JoinTreeCliqueNode)]
    # @property
    # def clique_nodes(self):
    #     return [n for n in self.nodes if isinstance(n, JoinTreeCliqueNode)]

    def get_graphviz_source(self, dpi=200, rankdir='LL'):
        fh = StringIO()
        fh.write('graph G {\n')
        fh.write('  graph [ dpi = %d bgcolor="transparent" rankdir="%s"];\n' % (dpi, rankdir))
        edges = set()
        for node in self.nodes:
            if isinstance(node, JoinTreeSepSetNode):
                fh.write('  %s [ shape="box" color="blue"];\n' % node.name)
            else:
                fh.write('  %s [ shape="ellipse" color="red"];\n' % node.name)
            for neighbour in node.neighbours:
                edge = [node.name, neighbour.name]
                edges.add(tuple(sorted(edge)))
        for source, target in edges:
            fh.write('  %s -- %s;\n' % (source, target))
        fh.write('}\n')
        return fh.getvalue()

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef initialize_potentials(self, dict assignments, BBN bbn, dict evidence={}):
        # Step 1, assign 1 to each cluster and sepset
        cdef dict tt
        cdef list vals
        cdef list variables
        cdef set domain
        cdef dict argvals
        cdef double potential
        for node in self.nodes:
            tt = dict()
            vals = []
            variables = node.variable_names
            # Lets sort the variables here so that
            # the variable names in the keys in
            # the tt are always sorted.
            variables.sort()
            for variable in variables:
                domain = bbn.domains.get(variable, [True, False])
                vals.append(list(product([variable], domain)))
            permutations = product(*vals)
            for permutation in permutations:
                tt[permutation] = 1
            node.potential_tt = tt

        # Step 2: Note that in H&D the assignments are
        # done as part of step 2 however we have
        # seperated the assignment algorithm out and
        # done these prior to step 1.
        # Now for each assignment we want to
        # generate a truth-table from the
        # values of the bbn truth-tables that are
        # assigned to the clusters...

        for clique, bbn_nodes in assignments.iteritems():

            tt = dict()
            vals = []
            variables = list(clique.variable_names)
            variables.sort()
            for variable in variables:
                domain = bbn.domains.get(variable, [True, False])
                vals.append(list(product([variable], domain)))
            permutations = product(*vals)
            for permutation in permutations:
                argvals = dict(permutation)
                potential = 1.0
                for bbn_node in bbn_nodes:
                    bbn_node.clique = clique
                    # We could handle evidence here
                    # by altering the potential_tt.
                    # This is slightly different to
                    # the way that H&D do it.

                    arg_list = []
                    for arg_name in get_args(bbn_node.func):
                        arg_list.append(argvals[arg_name])

                    potential *= bbn_node.func(*arg_list)
                tt[permutation] = potential
            clique.potential_tt = tt

        if not evidence:
            # We dont need to deal with likelihoods
            # if we dont have any evidence.
            return

        # Step 2b: Set each liklihood element ^V(v) to 1
        likelihoods = self.initial_likelihoods(assignments, bbn)
        for clique, bbn_nodes in assignments.iteritems():
            for node in bbn_nodes:
                if node.variable_name in evidence:
                    for k, v in clique.potential_tt.items():
                        # Encode the evidence in
                        # the clique potential...
                        for variable, value in k:
                            if (variable == node.variable_name):
                                if value != evidence[variable]:
                                    clique.potential_tt[k] = 0

    def initial_likelihoods(self, assignments, bbn):
        # TODO: Since this is the same every time we should probably
        # cache it.
        l = defaultdict(dict)
        for clique, bbn_nodes in assignments.iteritems():
            for node in bbn_nodes:
                for value in bbn.domains.get(
                        node.variable_name, [True, False]):
                    l[(node.variable_name, value)] = 1
        return l

    cdef dict assign_clusters(self, BBN bbn):
        cdef dict ret
        assignments_by_family = dict()
        assignments_by_clique = defaultdict(list)
        assigned = set()
        for node in bbn.nodes:
            args = get_args(node.func)
            if len(args) == 1:
                # If the func has only 1 arg
                # it means that it does not
                # specify a conditional probability
                # This is where H&D is a bit vague
                # but it seems to imply that we
                # do not assign it to any
                # clique.
                # Revising this for now as I dont
                # think its correct, I think
                # all CPTs need to be assigned
                # once and once only. The example
                # in H&D just happens to be a clique
                # that f_a could have been assigned
                # to but wasnt presumably because
                # it got assigned somewhere else.
                pass
                #continue
            # Now we need to find a cluster that
            # is a superset of the Family(v)
            # Family(v) is defined by D&H to
            # be the union of v and parents(v)
            family = set(args)
            # At this point we need to know which *variable*
            # a BBN node represents. Up to now we have
            # not *explicitely* specified this, however
            # we have been following some conventions
            # so we could just use this convention for
            # now. Need to come back to this to
            # perhaps establish the variable at
            # build bbn time...
            containing_cliques = [clique_node for clique_node in
                                  self.clique_nodes if
                                  (set(clique_node.variable_names).
                                   issuperset(family))]
            assert len(containing_cliques) >= 1
            for clique in containing_cliques:
                if node in assigned:
                    # Make sure we assign all original
                    # PMFs only once each
                    continue
                assignments_by_clique[clique].append(node)
                assigned.add(node)
            assignments_by_family[tuple(family)] = containing_cliques
        ret = <dict> assignments_by_clique
        # return assignments_by_clique
        return ret

    def propagate(self, starting_clique=None):
        '''Refer to H&D pg. 20'''

        # Step 1 is to choose an arbitrary clique cluster
        # as starting cluster
        if starting_clique is None:
            starting_clique = self.clique_nodes[0]

        # Step 2: Unmark all clusters, call collect_evidence(X)
        for node in self.clique_nodes:
            node.marked = False
        self.collect_evidence(sender=starting_clique)

        # Step 3: Unmark all clusters, call distribute_evidence(X)
        for node in self.clique_nodes:
            node.marked = False

        self.distribute_evidence(starting_clique)

    def collect_evidence(self, sender=None, receiver=None):

        # Step 1, Mark X
        sender.marked = True

        # Step 2, call collect_evidence on Xs unmarked
        # neighbouring clusters.
        for neighbouring_clique in sender.neighbouring_cliques:
            if not neighbouring_clique.marked:
                self.collect_evidence(
                    sender=neighbouring_clique,
                    receiver=sender)
        # Step 3, pass message from sender to receiver
        if receiver is not None:
            sender.pass_message(receiver)

    def distribute_evidence(self, sender=None, receiver=None):

        # Step 1, Mark X
        sender.marked = True

        # Step 2, pass a messagee from X to each of its
        # unmarked neighbouring clusters
        for neighbouring_clique in sender.neighbouring_cliques:
            if not neighbouring_clique.marked:
                sender.pass_message(neighbouring_clique)

        # Step 3, call distribute_evidence on Xs unmarked neighbours
        for neighbouring_clique in sender.neighbouring_cliques:
            if not neighbouring_clique.marked:
                self.distribute_evidence(
                    sender=neighbouring_clique,
                    receiver=sender)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef dict marginal(self, BBNNode bbn_node):
        '''Remember that the original
        variables that we are interested in
        are actually in the bbn. However
        when we constructed the JT we did
        it out of the moralized graph.
        This means the cliques refer to
        the nodes in the moralized graph
        and not the nodes in the BBN.
        For efficiency we should come back
        to this and add some pointers
        or an index.
        '''

        # First we will find the JT nodes that
        # contain the bbn_node ie all the nodes
        # that are either cliques or sepsets
        # that contain the bbn_node
        # Note that for efficiency we
        # should probably have an index
        # cached in the bbn and/or the jt.
        cdef tuple entry
        cdef list containing_nodes = []
        cdef dict ret

        for node in self.clique_nodes:
            if bbn_node.name in [n.name for n in node.clique.nodes]:
                containing_nodes.append(node)
                # In theory it doesnt matter which one we
                # use so we could bale out after we
                # find the first one
                # TODO: With some better indexing we could
                # avoid searching for this node every time...

        clique_node = containing_nodes[0]
        tt = defaultdict(float)
        for k, v in clique_node.potential_tt.items():
            entry = transform(
                k,
                clique_node.variable_names,
                [bbn_node.variable_name])
            tt[entry] += v

        # Now if this node was evidenced we need to normalize
        # over the values...
        # TODO: It will be safer to copy the defaultdict to a regular dict
        ret = <dict>tt
        return ret


cdef class Clique(object):
    cdef set nodes
    cdef JoinTreeCliqueNode node
    cdef dict potential_tt
    def __cinit__(self, set cluster):
        self.nodes = cluster
    property nodes:
        def __get__(self):
            return self.nodes
        def __set__(self, set nodes ):
            self.nodes = nodes
    property node:
        def __get__(self):
            return self.node
        def __set__(self, JoinTreeCliqueNode node ):
            self.node = node
    property potential_tt:
        def __get__(self):
            return self.potential_tt
        def __set__(self, dict potential_tt ):
            self.potential_tt = potential_tt

    def __repr__(self):
        vars = sorted([n.variable_name for n in self.nodes])
        # for n in self.nodes:
        #     print('%s:%s' % (n.name, str(n.variable_name)))
        return 'Clique_%s' % ''.join([v.upper() for v in vars])


cdef tuple transform(tuple x, list X, list R):
    '''Transform a Potential Truth Table
    Entry into a different variable space.
    For example if we have the
    entry [True, True, False] representing
    values of variable [A, B, C] in X
    and we want to transform into
    R which has variables [C, A] we
    will return the entry [False, True].
    Here X represents the argument list
    for the clique set X and R represents
    the argument list for the sepset.
    This implies that R is always a subset
    of X'''
    cdef list entry = []
    cdef int pos
    for r in R:
        pos = X.index(r)
        entry.append(x[pos])
    return tuple(entry)


cdef class JoinTreeCliqueNode(object):
    cdef Clique clique
    cdef str name
    cdef list neighbours
    cdef dict potential_tt
    cdef dict potential_tt_old
    cdef bool marked
    def __cinit__(self,  Clique clique, list neighbours=[]):
        self.name = clique.__repr__()
        self.clique = clique
        self.neighbours = neighbours[:]
    property clique:
        def __get__(self):
            return self.clique
        def __set__(self, Clique clique ):
            self.clique = clique
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name ):
            self.name = name
    property neighbours:
        def __get__(self):
            return self.neighbours
        def __set__(self, list neighbours):
            self.neighbours = neighbours
    property potential_tt:
        def __get__(self):
            return self.potential_tt
        def __set__(self, dict potential_tt):
            self.potential_tt = potential_tt
    property potential_tt_old:
        def __get__(self):
            return self.potential_tt_old
        def __set__(self, dict potential_tt_old):
            self.potential_tt_old = potential_tt_old
    property marked:
        def __get__(self):
            return self.marked
        def __set__(self, bool marked):
            self.marked = marked

    property variable_names:
        def __get__(self):
            var_names = []
            for node in self.clique.nodes:
                var_names.append(node.variable_name)
            return sorted(var_names)

    # @property
    # def variable_names(self):
    #     '''Return the set of variable names
    #     that this clique represents'''
    #     var_names = []
    #     for node in self.clique.nodes:
    #         var_names.append(node.variable_name)
    #     return sorted(var_names)
    property neighbouring_cliques:
        def __get__(self):
            neighbours = set()
            for sepset_node in self.neighbours:
                # All *immediate* neighbours will
                # be sepset nodes, its the neighbours of
                # these sepsets that form the nodes
                # clique neighbours (excluding itself)
                for clique_node in sepset_node.neighbours:
                    if clique_node is not self:
                        neighbours.add(clique_node)
            return neighbours

    # @property
    # def neighbouring_cliques(self):
    #     '''Return the neighbouring cliques
    #     this is used during the propagation algorithm.
    #
    #     '''
    #     neighbours = set()
    #     for sepset_node in self.neighbours:
    #         # All *immediate* neighbours will
    #         # be sepset nodes, its the neighbours of
    #         # these sepsets that form the nodes
    #         # clique neighbours (excluding itself)
    #         for clique_node in sepset_node.neighbours:
    #             if clique_node is not self:
    #                 neighbours.add(clique_node)
    #     return neighbours

    def pass_message(self, target):
        self._pass_message(target)
    cdef _pass_message(self, JoinTreeCliqueNode target):
        '''Pass a message from this node to the
        recipient node during propagation.

        NB: It may turnout at this point that
        after initializing the potential
        Truth table on the JT we could quite
        simply construct a factor graph
        from the JT and use the factor
        graph sum product propagation.
        In theory this should be the same
        and since the semantics are already
        worked out it would be easier.'''

        cdef JoinTreeSepSetNode sepset_node
        # Find the sepset node between the
        # source and target nodes.
        sepset_node = list(set(self.neighbours).intersection(
            target.neighbours))[0]

        # Step 1: projection
        self.project(sepset_node)

        # Step 2 absorbtion
        self.absorb(sepset_node, target)

    def project(self, sepset_node):
        self._project(sepset_node)
    cdef _project(self, JoinTreeSepSetNode sepset_node):
        '''See page 20 of PPTC.
        We assign a new potential tt to
        the sepset which consists of the
        potential of the source node
        with all variables not in R marginalized.
        '''
        cdef tuple entry
        assert sepset_node in self.neighbours
        # First we make a copy of the
        # old potential tt
        sepset_node.potential_tt_old = <dict>copy.deepcopy(
            sepset_node.potential_tt)

        # Now we assign a new potential tt
        # to the sepset by marginalizing
        # out the variables from X that are not
        # in the sepset
        tt = defaultdict(float)
        for k, v in self.potential_tt.items():
            entry = transform(k, self.variable_names,
                              sepset_node.variable_names)
            tt[entry] += v
        sepset_node.potential_tt = <dict>tt

    def absorb(self, sepset, target):
        self._absorb( sepset, target)
    cdef _absorb(self, JoinTreeSepSetNode sepset, JoinTreeCliqueNode target):
        # Assign a new potential tt to
        # Y (the target)
        cdef dict tt = dict()
        cdef tuple entry
        for k, v in target.potential_tt.items():
            # For each entry we multiply by
            # sepsets new value and divide
            # by sepsets old value...
            # Note that nowhere in H&D is
            # division on potentials defined.
            # However in Barber page 12
            # an equation implies that
            # the the division is equivalent
            # to the original assignment.
            # For now we will assume entry-wise
            # division which seems logical.
            entry = transform(k, target.variable_names,
                              sepset.variable_names)
            if target.potential_tt[k] == 0:
                tt[k] = 0
            else:
                tt[k] = target.potential_tt[k] * (
                    sepset.potential_tt[entry] /
                    sepset.potential_tt_old[entry])
        target.potential_tt = tt

    def __repr__(self):
        return '<JoinTreeCliqueNode: %s>' % self.clique


cdef class SepSet(object):
    cdef Clique X
    cdef Clique Y
    cdef list label
    def __cinit__(self, Clique X, Clique Y):
        '''X and Y are cliques represented as sets.'''
        self.X = X
        self.Y = Y
        self.label = list(X.nodes.intersection(Y.nodes))
    property mass:
        def __get__(self):
            return len(self.label)

    # @property
    # def mass(self):
    #     return len(self.label)
    property cost:
        def __get__(self):
            return 2 ** len(self.X.nodes) + 2 ** len(self.Y.nodes)

    # @property
    # def cost(self):
    #     '''Since cost is used as a tie-breaker
    #     and is an optimization for inference time
    #     we will punt on it for now. Instead we
    #     will just use the assumption that all
    #     variables in X and Y are binary and thus
    #     use a weight of 2.
    #     TODO: come back to this and compute
    #     actual weights
    #     '''
    #     return 2 ** len(self.X.nodes) + 2 ** len(self.Y.nodes)

    def insertable(self, forest):
        return self._insertable(forest)
    cdef bool _insertable(self, set forest):
        '''A sepset can only be inserted
        into the JT if the cliques it
        separates are NOT already on
        the same tree.
        NOTE: For efficiency we should
        add an index that indexes cliques
        into the trees in the forest.'''
        cdef list X_trees = [t for t in forest if self.X in
                   [n.clique for n in t.clique_nodes]]
        cdef list Y_trees = [t for t in forest if self.Y in
                   [n.clique for n in t.clique_nodes]]
        assert len(X_trees) == 1
        assert len(Y_trees) == 1
        if X_trees[0] is not Y_trees[0]:
            return True
        return False

    def insert(self, forest):
        self._insert(forest)
    cdef _insert(self, set forest):
        '''Inserting this sepset into
        a forest, providing the two
        cliques are in different trees,
        means that effectively we are
        collapsing the two trees into
        one. We will explicitely perform
        this collapse by adding the
        sepset node into the tree
        and adding edges between itself
        and its clique node neighbours.
        Finally we must remove the
        second tree from the forest
        as it is now joined to the
        first.
        '''
        cdef JoinTree X_tree = [t for t in forest if self.X in
                  [n.clique for n in t.clique_nodes]][0]
        cdef JoinTree Y_tree = [t for t in forest if self.Y in
                  [n.clique for n in t.clique_nodes]][0]

        # Now create and insert a sepset node into the Xtree
        cdef JoinTreeSepSetNode ss_node = JoinTreeSepSetNode(self.__repr__(), self)
        X_tree.nodes.append(ss_node)

        # And connect them
        self.X.node.neighbours.append(ss_node)
        ss_node.neighbours.append(self.X.node)

        # Now lets keep the X_tree and drop the Y_tree
        # this means we need to copy all the nodes
        # in the Y_tree that are not already in the X_tree
        for node in Y_tree.nodes:
            if node in X_tree.nodes:
                continue
            X_tree.nodes.append(node)

        # Now connect the sepset node to the
        # Y_node (now residing in the X_tree)
        self.Y.node.neighbours.append(ss_node)
        ss_node.neighbours.append(self.Y.node)

        # And finally we must remove the Y_tree from
        # the forest...
        forest.remove(Y_tree)

    def __repr__(self):
        return 'SepSet_%s' % ''.join(
            #[x.name[2:].upper() for x in list(self.label)])
            [x.variable_name.upper() for x in list(self.label)])


cdef class JoinTreeSepSetNode(object):
    cdef str name
    cdef list neighbours
    cdef SepSet sepset
    cdef dict potential_tt
    cdef dict potential_tt_old
    cdef bool marked
    def __cinit__(self, str name, SepSet sepset, list neighbours=[]):
        self.name = name
        self.sepset = sepset
        self.neighbours = neighbours[:]
    property name:
        def __get__(self):
            return self.name
        def __set__(self, str name ):
            self.name = name
    property sepset:
        def __get__(self):
            return self.sepset
        def __set__(self, SepSet sepset ):
            self.sepset = sepset
    property neighbours:
        def __get__(self):
            return self.neighbours
        def __set__(self, list neighbours):
            self.neighbours = neighbours
    property potential_tt:
        def __get__(self):
            return self.potential_tt
        def __set__(self, dict potential_tt):
            self.potential_tt = potential_tt
    property potential_tt_old:
        def __get__(self):
            return self.potential_tt_old
        def __set__(self, dict potential_tt_old):
            self.potential_tt_old = potential_tt_old
    property marked:
        def __get__(self):
            return self.marked
        def __set__(self, bool marked):
            self.marked = marked

    property variable_names:
        def __get__(self):
            return sorted([x.variable_name for x in self.sepset.label])

    # @property
    # def variable_names(self):
    #     '''Return the set of variable names
    #     that this sepset represents'''
    #     # TODO: we are assuming here
    #     # that X and Y are each separate
    #     # variables from the BBN which means
    #     # we are assuming that the sepsets
    #     # always contain only 2 nodes.
    #     # Need to check whether this is
    #     # the case.
    #     return sorted([x.variable_name for x in self.sepset.label])

    def __repr__(self):
        return '<JoinTreeSepSetNode: %s>' % self.sepset

def build_bbn(*args, **kwds):
    return _build_bbn(args, kwds)

cdef BBN _build_bbn(tuple args, dict kwds):
    '''Builds a BBN Graph from
    a list of functions and domains'''
    cdef set variables = set()
    cdef dict domains = kwds.get('domains', {})
    cdef str name = kwds.get('name')
    cdef dict variable_nodes = dict()
    cdef dict factor_nodes = dict()
    cdef list factor_args
    # cdef BBNNode bbn_node
    cdef dict original_factors
    cdef list parents
    cdef BBN bbn
    if isinstance(args[0], list):
        # Assume the functions were all
        # passed in a list in the first
        # argument. This makes it possible
        # to build very large graphs with
        # more than 255 functions, since
        # Python functions are limited to
        # 255 arguments.
        args = args[0]

    for factor in args:
        factor_args = get_args(factor)
        variables.update(factor_args)
        # bbn_node = BBNNode(factor.__name__, [], [], factor)
        factor_nodes[factor.__name__] = BBNNode(factor.__name__, factor)

    # Now lets create the connections
    # To do this we need to find the
    # factor node representing the variables
    # in a child factors argument and connect
    # it to the child node.

    # Note that calling original_factors
    # here can break build_bbn if the
    # factors do not correctly represent
    # a BBN.
    original_factors = get_original_factors(factor_nodes.values())
    for factor_node in factor_nodes.values():
        factor_args = get_args(factor_node)
        parents = [original_factors[arg] for arg in
                   factor_args if original_factors[arg] != factor_node]
        for parent in parents:
            connect(parent, factor_node)
    bbn = BBN(original_factors, name=name)
    bbn.domains = domains

    return bbn




def get_original_factors(factors):
    return _get_original_factors(factors)
cdef dict _get_original_factors(list factors):
    '''
    For a set of factors, we want to
    get a mapping of the variables to
    the factor which first introduces the
    variable to the set.
    To do this without enforcing a special
    naming convention such as 'f_' for factors,
    or a special ordering, such as the last
    argument is always the new variable,
    we will have to discover the 'original'
    factor that introduces the variable
    iteratively.
    '''
    cdef dict original_factors = dict()
    cdef list args
    cdef list unaccounted_args
    while len(original_factors) < len(factors):
        for factor in factors:
            args = get_args(factor)
            unaccounted_args = [a for a in args if a not in original_factors]
            if len(unaccounted_args) == 1:
                original_factors[unaccounted_args[0]] = factor
    return original_factors

def make_node_func(variable_name, conditions):
    # We will enforce the following
    # convention.
    # The ordering of arguments will
    # be firstly the parent variables
    # in alphabetical order, followed
    # always by the child variable
    tt = dict()
    domain = set()
    for givens, conditionals in conditions:
        key = []
        for parent_name, val in sorted(givens):
            key.append((parent_name, val))
        # Now we will sort the
        # key before we add the child
        # node.
        #key.sort(key=lambda x: x[0])

        # Now for each value in
        # the conditional probabilities
        # we will add a new key
        for value, prob in conditionals.items():
            key_ = tuple(key + [(variable_name, value)])
            domain.add(value)
            tt[key_] = prob

    argspec = [k[0] for k in key_]

    def node_func(*args):
        key = []
        for arg, val in zip(argspec, args):
            key.append((arg, val))
        return tt[tuple(key)]
    node_func.argspec = argspec
    node_func._domain = domain
    node_func.__name__ = 'f_' + str(variable_name)
    return node_func


def build_bbn_from_conditionals(conds):
    node_funcs = []
    domains = dict()
    for variable_name, cond_tt in conds.items():
        node_func = make_node_func(variable_name, cond_tt)
        node_funcs.append(node_func)
        domains[variable_name] = node_func._domain
    node_funcs = tuple(node_funcs)
    return build_bbn(*node_funcs, domains=domains)


cdef UndirectedGraph make_undirected_copy(BBN dag):
    '''Returns an exact copy of the dag
    except that direction of edges are dropped.'''
    cdef dict nodes = dict()
    cdef UndirectedNode undirected_node
    cdef UndirectedGraph g
    for node in dag.nodes:
        undirected_node = UndirectedNode(
            name=node.name)
        undirected_node.func = node.func
        undirected_node.argspec = node.argspec
        undirected_node.variable_name = node.variable_name
        nodes[node.name] = undirected_node
    # Now we need to traverse the original
    # nodes once more and add any parents
    # or children as neighbours.
    for node in dag.nodes:
        for parent in node.parents:
            nodes[node.name].neighbours.append(
                nodes[parent.name])
            nodes[parent.name].neighbours.append(
                nodes[node.name])

    g = UndirectedGraph(nodes.values())
    return g


cdef UndirectedGraph make_moralized_copy(UndirectedGraph gu, BBN dag):
    '''gu is an undirected graph being
    a copy of dag.'''
    cdef UndirectedGraph gm = copy.deepcopy(gu)
    cdef dict gm_nodes = dict(
        [(node.name, node) for node in gm.nodes])
    for node in dag.nodes:
        for parent_1, parent_2 in combinations(
                node.parents, 2):
            if gm_nodes[parent_1.name] not in \
               gm_nodes[parent_2.name].neighbours:
                gm_nodes[parent_2.name].neighbours.append(
                    gm_nodes[parent_1.name])
            if gm_nodes[parent_2.name] not in \
               gm_nodes[parent_1.name].neighbours:
                gm_nodes[parent_1.name].neighbours.append(
                    gm_nodes[parent_2.name])
    return gm


def priority_func(node):
    '''Specify the rules for computing
    priority of a node. See Harwiche and Wang pg 12.
    '''
    # We need to calculate the number of edges
    # that would be added.
    # For each node, we need to connect all
    # of the nodes in itself and its neighbours
    # (the "cluster") which are not already
    # connected. This will be the primary
    # key value in the heap.
    # We need to fix the secondary key, right
    # now its just 2 (because mostly the variables
    # will be discrete binary)
    introduced_arcs = 0
    cluster = [node] + node.neighbours
    for node_a, node_b in combinations(cluster, 2):
        if node_a not in node_b.neighbours:
            assert node_b not in node_a.neighbours
            introduced_arcs += 1
    return [introduced_arcs, 2]  # TODO: Fix this to look at domains


cdef list construct_priority_queue(dict nodes, object priority_func=priority_func):
    cdef list pq = []
    cdef list entry
    for node_name, node in nodes.iteritems():
        entry = priority_func(node) + [node.name]
        heapq.heappush(pq, entry)
    return pq


cdef record_cliques(list cliques, set cluster):
    '''We only want to save the cluster
    if it is not a subset of any clique
    already saved.
    Argument cluster must be a set'''
    if any([cluster.issubset(c.nodes) for c in cliques]):
        return
    cliques.append(Clique(cluster))


cdef tuple triangulate(UndirectedGraph gm, object priority_func=priority_func):
    '''Triangulate the moralized Graph. (in Place)
    and return the cliques of the triangulated
    graph as well as the elimination ordering.'''
    # First we will make a copy of gm...
    cdef UndirectedGraph gm_ = copy.deepcopy(gm)

    # Now we will construct a priority q using
    # the standard library heapq module.
    # See docs for example of priority q tie
    # breaking. We will use a 3 element list
    # with entries as follows:
    #   - Number of edges added if V were selected
    #   - Weight of V (or cluster)
    #   - Pointer to node in gm_
    # Note that its unclear from Huang and Darwiche
    # what is meant by the "number of values of V"
    cdef dict gmnodes = dict([(node.name, node) for node in gm.nodes])
    cdef list elimination_ordering = []
    cdef list cliques = []
    cdef dict gm_nodes
    cdef list pq
    cdef set gmcluster
    while True:
        gm_nodes = dict([(node.name, node) for node in gm_.nodes])
        if not gm_nodes:
            break
        pq = construct_priority_queue(gm_nodes, priority_func)
        # Now we select the first node in
        # the priority q and any arcs that
        # should be added in order to fully connect
        # the cluster should be added to both
        # gm and gm_
        v = gm_nodes[pq[0][2]]
        cluster = [v] + v.neighbours
        for node_a, node_b in combinations(cluster, 2):
            if node_a not in node_b.neighbours:
                node_b.neighbours.append(node_a)
                node_a.neighbours.append(node_b)
                # Now also add this new arc to gm...
                gmnodes[node_b.name].neighbours.append(
                    gmnodes[node_a.name])
                gmnodes[node_a.name].neighbours.append(
                    gmnodes[node_b.name])
        gmcluster = set([gmnodes[c.name] for c in cluster])
        record_cliques(cliques, gmcluster)
        # Now we need to remove v from gm_...
        # This means we also have to remove it from all
        # of its neighbours that reference it...
        for neighbour in v.neighbours:
            neighbour.neighbours.remove(v)
        gm_.nodes.remove(v)
        elimination_ordering.append(v.name)
    return cliques, elimination_ordering


cdef JoinTree build_join_tree(BBN dag, object clique_priority_func=priority_func):

    # First we will create an undirected copy
    # of the dag
    cdef UndirectedGraph gu = make_undirected_copy(dag)

    # Now we create a copy of the undirected graph
    # and connect all pairs of parents that are
    # not already parents called the 'moralized' graph.
    cdef UndirectedGraph gm = make_moralized_copy(gu, dag)
    cdef list cliques
    cdef list elimination_ordering
    cdef set forest
    cdef JoinTreeCliqueNode jt_node
    cdef set S
    cdef long sepsets_inserted
    cdef list deco
    cdef JoinTree jt
    # Now we triangulate the moralized graph...
    cliques, elimination_ordering = triangulate(gm, clique_priority_func)

    # Now we initialize the forest and sepsets
    # Its unclear from Darwiche Huang whether we
    # track a sepset for each tree or whether its
    # a global list????
    # We will implement the Join Tree as an undirected
    # graph for now...

    # First initialize a set of graphs where
    # each graph initially consists of just one
    # node for the clique. As these graphs get
    # populated with sepsets connecting them
    # they should collapse into a single tree.
    forest = set()
    for clique in cliques:
        jt_node = JoinTreeCliqueNode(clique)
        # Track a reference from the clique
        # itself to the node, this will be
        # handy later... (alternately we
        # could just collapse clique and clique
        # node into one class...
        clique.node = jt_node
        tree = JoinTree([jt_node])
        forest.add(tree)

    # Initialize the SepSets
    S = set()  # track the sepsets
    for X, Y in combinations(cliques, 2):
        if X.nodes.intersection(Y.nodes):
            S.add(SepSet(X, Y))
    sepsets_inserted = 0
    while sepsets_inserted < (len(cliques) - 1):
        # Adding in name to make this sort deterministic
        deco = [(s, -1 * s.mass, s.cost, s.__repr__()) for s in S]
        deco.sort(key=lambda x: x[1:])
        if len(deco) > 0:
            candidate_sepset = deco[0][0]
            for candidate_sepset, _, _, _ in deco:
                if candidate_sepset.insertable(forest):
                    # Insert into forest and remove the sepset
                    candidate_sepset.insert(forest)
                    S.remove(candidate_sepset)
                    sepsets_inserted += 1
                    break

    assert len(forest) == 1
    jt = list(forest)[0]
    return jt
