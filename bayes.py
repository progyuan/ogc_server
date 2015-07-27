# -*- coding: utf-8 -*-
import os, sys, codecs
import itertools
import json
import bayesian
from bayesian.bbn import *
from bayesian.factor_graph import *
import pymongo
from bson.objectid import ObjectId



ENCODING = 'utf-8'
ENCODING1 = 'gb18030'
def dec(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_encode(aStr, 'replace')
    return text
def dec1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_encode(aStr, 'replace')
    return text

class BBNPlus(BBN):
    def __init__(self, nodes_dict, name=None, domains={}):
        BBN.__init__(self, nodes_dict, name=None, domains={})
    def get_graphviz_source_plus(self):
        fh = StringIO()
        fh.write('digraph G {\n')
        fh.write('  graph [ dpi = 100 bgcolor="transparent" rankdir="LR"];\n')
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

class FactorGraphPlus(FactorGraph):
    def __init__(self, nodes, name=None, n_samples=100):
        FactorGraph.__init__(self, nodes, name=None, n_samples=100)
    def export_plus(self, filename=None, format='graphviz'):
        '''Export the graph in GraphViz dot language.'''
        fh = None
        if filename:
            fh = open(filename, 'w')
        else:
            fh = sys.stdout
        if format != 'graphviz':
            raise 'Unsupported Export Format.'
        fh.write('graph G {\n')
        fh.write('  graph [ dpi = 100 bgcolor="transparent" rankdir="LR"];\n')
        edges = set()
        for node in self.nodes:
            if isinstance(node, FactorNode):
                fh.write('  %s [ shape="rectangle" color="red"];\n' % node.name)
            else:
                fh.write('  %s [ shape="ellipse" color="blue"];\n' % node.name)
        for node in self.nodes:
            for neighbour in node.neighbours:
                edge = [node.name, neighbour.name]
                edge = tuple(sorted(edge))
                edges.add(edge)
        for source, target in edges:
            fh.write('  %s -- %s;\n' % (source, target))
        fh.write('}\n')
        if filename and fh:
            fh.close()

def build_graph_plus(*args, **kwds):
    variables = set()
    domains = kwds.get('domains', {})
    name = kwds.get('name')
    variable_nodes = dict()
    factor_nodes = []
    if isinstance(args[0], list):
        # Assume the functions were all
        # passed in a list in the first
        # argument. This makes it possible
        # to build very large graphs with
        # more than 255 functions.
        args = args[0]
    for factor in args:
        factor_args = get_args(factor)
        variables.update(factor_args)
        factor_node = FactorNode(factor.__name__, factor)
        #factor_node.func.domains = domains
        # Bit of a hack for now we should actually exclude variables that
        # are not parameters of this function
        factor_nodes.append(factor_node)
    for variable in variables:
        node = VariableNode(
            variable,
            domain=domains.get(variable, [True, False]))
        variable_nodes[variable] = node
    # Now we have to connect each factor node
    # to its variable nodes
    for factor_node in factor_nodes:
        factor_args = get_args(factor_node.func)
        bayesian.factor_graph.connect(factor_node, [variable_nodes[x] for x in factor_args])
    graph = FactorGraphPlus(variable_nodes.values() + factor_nodes, name=name)
    #print domains
    return graph

def build_bbn_plus(*args, **kwds):
    '''Builds a BBN Graph from
    a list of functions and domains'''
    variables = set()
    domains = kwds.get('domains', {})
    name = kwds.get('name')
    variable_nodes = dict()
    factor_nodes = dict()

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
        bbn_node = BBNNode(factor)
        factor_nodes[factor.__name__] = bbn_node

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
            bayesian.graph.connect(parent, factor_node)
    bbn = BBNPlus(original_factors, name=name)
    bbn.domains = domains

    return bbn

def build_bbn_from_conditionals_plus(conds):
    node_funcs = []
    domains = dict()
    for variable_name, cond_tt in conds.items():
        node_func = make_node_func(variable_name, cond_tt)
        node_funcs.append(node_func)
        domains[variable_name] = node_func._domain
    return build_bbn_plus(*node_funcs, domains=domains)

def build_graph_from_conditionals_plus(conds):
    node_funcs = []
    domains = dict()
    for variable_name, cond_tt in conds.items():
        node_func = make_node_func(variable_name, cond_tt)
        node_funcs.append(node_func)
        domains[variable_name] = node_func._domain
    return build_graph_plus(*node_funcs, domains=domains)


def close_enough(x, y, r=3):
    return round(x, r) == round(y, r)

def test(cancer_graph):
    '''Column 2 of upper half of table'''

    result = cancer_graph.query()
    assert close_enough(result[('P', 'high')], 0.1)
    assert close_enough(result[('P', 'low')], 0.9)
    assert close_enough(result[('S', True)], 0.3)
    assert close_enough(result[('S', False)], 0.7)
    assert close_enough(result[('C', True)], 0.012)
    assert close_enough(result[('C', False)], 0.988)
    assert close_enough(result[('X', True)], 0.208)
    assert close_enough(result[('X', False)], 0.792)
    assert close_enough(result[('D', True)], 0.304)
    assert close_enough(result[('D', False)], 0.696)

# def test_D_True(self, cancer_graph):
    '''Column 3 of upper half of table'''
    result = cancer_graph.query(D=True)
    assert close_enough(result[('P', 'high')], 0.102)
    assert close_enough(result[('P', 'low')], 0.898)
    assert close_enough(result[('S', True)], 0.307)
    assert close_enough(result[('S', False)], 0.693)
    assert close_enough(result[('C', True)], 0.025)
    assert close_enough(result[('C', False)], 0.975)
    assert close_enough(result[('X', True)], 0.217)
    assert close_enough(result[('X', False)], 0.783)
    assert close_enough(result[('D', True)], 1)
    assert close_enough(result[('D', False)], 0)

# def test_S_True(self, cancer_graph):
    '''Column 4 of upper half of table'''
    result = cancer_graph.query(S=True)
    assert close_enough(result[('P', 'high')], 0.1)
    assert close_enough(result[('P', 'low')], 0.9)
    assert close_enough(result[('S', True)], 1)
    assert close_enough(result[('S', False)], 0)
    assert close_enough(result[('C', True)], 0.032)
    assert close_enough(result[('C', False)], 0.968)
    assert close_enough(result[('X', True)], 0.222)
    assert close_enough(result[('X', False)], 0.778)
    assert close_enough(result[('D', True)], 0.311)
    assert close_enough(result[('D', False)], 0.689)

# def test_C_True(self, cancer_graph):
    '''Column 5 of upper half of table'''
    result = cancer_graph.query(C=True)
    assert close_enough(result[('P', 'high')], 0.249)
    assert close_enough(result[('P', 'low')], 0.751)
    assert close_enough(result[('S', True)], 0.825)
    assert close_enough(result[('S', False)], 0.175)
    assert close_enough(result[('C', True)], 1)
    assert close_enough(result[('C', False)], 0)
    assert close_enough(result[('X', True)], 0.9)
    assert close_enough(result[('X', False)], 0.1)
    assert close_enough(result[('D', True)], 0.650)
    assert close_enough(result[('D', False)], 0.350)

# def test_C_True_S_True(self, cancer_graph):
    '''Column 6 of upper half of table'''
    result = cancer_graph.query(C=True, S=True)
    assert close_enough(result[('P', 'high')], 0.156)
    assert close_enough(result[('P', 'low')], 0.844)
    assert close_enough(result[('S', True)], 1)
    assert close_enough(result[('S', False)], 0)
    assert close_enough(result[('C', True)], 1)
    assert close_enough(result[('C', False)], 0)
    assert close_enough(result[('X', True)], 0.9)
    assert close_enough(result[('X', False)], 0.1)
    assert close_enough(result[('D', True)], 0.650)
    assert close_enough(result[('D', False)], 0.350)

# def test_D_True_S_True(self, cancer_graph):
    '''Column 7 of upper half of table'''
    result = cancer_graph.query(D=True, S=True)
    assert close_enough(result[('P', 'high')], 0.102)
    assert close_enough(result[('P', 'low')], 0.898)
    assert close_enough(result[('S', True)], 1)
    assert close_enough(result[('S', False)], 0)
    assert close_enough(result[('C', True)], 0.067)
    assert close_enough(result[('C', False)], 0.933)
    assert close_enough(result[('X', True)], 0.247)
    assert close_enough(result[('X', False)], 0.753)
    assert close_enough(result[('D', True)], 1)
    assert close_enough(result[('D', False)], 0)

def build_cancer_condition():
    cond = {
        'P':[
            [[],{'high':0.1,'low':0.9}]
        ],
        'S':[
            [[],{True:0.3, False:0.7}]
        ],
        'C':[
            [[['P', 'high'], ['S', True]], {
                True: 0.05,
                False: 0.95
            }],
            [[['P', 'high'], ['S', False]], {
                True: 0.02,
                False: 0.98
            }],
            [[['P', 'low'], ['S', True]], {
                True: 0.03,
                False: 0.97
            }],
            [[['P', 'low'], ['S', False]], {
                True: 0.001,
                False: 0.999
            }],
        ],
        'X':[
            [[['C', True]], {
                True: 0.9,
                False: 0.1
            }],
            [[['C', False]], {
                True: 0.2,
                False: 0.8
            }],
        ],
        'D':[
            [[['C', True]], {
                True: 0.65,
                False: 0.35
            }],
            [[['C', False]], {
                True: 0.3,
                False: 0.7
            }],
        ],
    }
    return cond

def get_collection(collection):
    ret = None
    client = pymongo.MongoClient('192.168.1.8', 27017)
    db = client['kmgd']
    if not collection in db.collection_names(False):
        ret = db.create_collection(collection)
    else:
        ret = db[collection]
    return ret

def get_state_examination_data_by_line_name(line_name):
    collection = get_collection('state_examination')
    return list(collection.find({'line_name':line_name}))

def build_state_examination_condition(line_name):
    def calc_probability1(data, field_name, field_value):
        def filterfunc(item):
            return item[field_name] == field_value
        ret = 0.0
        cnt = len(data)
        l = filter(filterfunc, data)
        if cnt > 0:
            ret = float(len(l))/float(cnt)
        return ret

    def calc_probability2(data, *args):#[{'name':'aaa', 'value':'I'},{'name':'bbb', 'value':'II'}]
        def filterfunc(item):
            ret = True
            for i in args:
                ret = ret and (item[i['name']] == i['value'])
            return ret
        ret = 0.0
        cnt = len(data)
        l = filter(filterfunc, data)
        if cnt > 0:
            ret = float(len(l))/float(cnt)
        return ret


    def calc_probability_combo(data, *args):#[{'name':'aaa', 'range':['I', 'II', 'III', 'IV']}{'name':'bbb', 'range':['I', 'II', 'III', 'IV']}]
        def pairwise(iterable):
            for (i, thing) in enumerate(iterable):
                if i % 2 == 0:
                    yield [thing, iterable[i+1]]
        def dictwise(iterable):
            for (i, thing) in enumerate(iterable):
                if i % 2 == 0:
                    yield {'name':thing, 'value':iterable[i+1]}
        retname, retlist = '', []
        args = list(args)
        name0 = args[0]['name']
        range0 = args[0]['range']
        args1 = args[:]
        del args1[0]
        namelist1 = [[i['name'],] for i in args1]
        rangelist1 = [i['range'] for i in args1]
        for i in args:
            retname += '%s$' % i['name']
        retname = retname[:-1]
        t = zip(namelist1, rangelist1)
        t = list(itertools.chain.from_iterable(t))
        # print(t)
        iterlist = itertools.product(*t)
        for i in iterlist:
            l = []
            p = pairwise(i)
            # pp = list(p)
            # print(pp)
            l.append(list(p))
            d = dictwise(i)
            o = {}
            for j in range0:
                dd = [{'name':name0, 'value':j}]
                for k in d:
                    dd.append(k)
                print(dd)
                o[j] = calc_probability2(data, *dd)
            l.append(o)
            retlist.append(l)


        return retname, retlist

    def calc_probability_combo_line_unit(data, unit_index):
        return calc_probability_combo(data, {'name':'line_state', 'range':['I', 'II', 'III', 'IV']}, {'name':'unit_%d' % unit_index, 'range':['I', 'II', 'III', 'IV']})

    data = get_state_examination_data_by_line_name(line_name)
    cond = {}
    for i in range(1, 9):
        cond['unit_%d' % i] = [
            [[],{
                'I':  calc_probability1(data, 'unit_%d' % i, 'I'),
                'II': calc_probability1(data, 'unit_%d' % i, 'II'),
                'III':calc_probability1(data, 'unit_%d' % i, 'III'),
                'IV': calc_probability1(data, 'unit_%d' % i, 'IV'),
                 }
             ]
        ]
    cond['line_state'] = [
        [[],{
            'I':  calc_probability1(data, 'line_state', 'I'),
            'II': calc_probability1(data, 'line_state', 'II'),
            'III':calc_probability1(data, 'line_state', 'III'),
            'IV': calc_probability1(data, 'line_state', 'IV'),
             }
         ]
    ]
    for i in range(1, 9):
        retname, retlist = calc_probability_combo_line_unit(data, i)
        cond[retname] = retlist
    return cond


def test_se():
    cond = build_state_examination_condition(u'七罗I回线')
    # print(cond.keys())
    s = json.dumps(cond,  ensure_ascii=True, indent=4)
    print(s)
    g = build_bbn_from_conditionals_plus(cond)
    print(g.get_graphviz_source_plus())
    # fg = build_graph_from_conditionals_plus(cond)
    # print(fg.export_plus(None))

def test_bayes():
    cond = build_cancer_condition()
    g = build_bbn_from_conditionals_plus(cond)
    # test(g)
    # g = build_bbn_plus(
    #     fP, fS, fC, fX, fD,
    #     domains={
    #         'P': ['low', 'high']})
    print(g.get_graphviz_source_plus())
    fg = build_graph_from_conditionals_plus(cond)
    # fg = build_graph_plus(
    #     fP, fS, fC, fX, fD,
    #     domains={
    #         'P': ['low', 'high']})
    print(fg.export_plus(None))
    # # g.q()
    # # g.q(P='high')
    # # g.q(D=True)
    # # g.q(S=True)
    # # g.q(C=True, S=True)
    # # g.q(D=True, S=True)
    # # print(g.factor_nodes())
    # # print(fg.export(None))


    # print(g.get_graphviz_source())
    # g.q()


if __name__ == '__main__':
    test_se()
