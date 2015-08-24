# -*- coding: utf-8 -*-
import os, sys, codecs
import time
import itertools
from collections import OrderedDict
import json
import numpy as np
import bayesian
#

from bayesian.factor_graph import *
import pymongo
from bson.code import Code
from bson.objectid import ObjectId
import xlrd, xlwt
from module_locator import enc, enc1, dec, dec1

USE_C_MODULE = False
try:
    from bayesian._bbn import *
    USE_C_MODULE = True
except:
    from bayesian.bbn import *

UNIT_NAME_MAPPING = {
    'unit_1': u'基础',
    'unit_2': u'杆塔',
    'unit_3': u'导地线',
    'unit_4': u'绝缘子串',
    'unit_5': u'金具',
    'unit_6': u'接地装置',
    'unit_7': u'附属设施',
    'unit_8': u'通道环境',
}
P_LINE_UNIT_PATH = ur'PROBABILITY_LINE_UNIT.json'
P_LINE_UNIT_PATH1 = ur'PROBABILITY_LINE_UNIT1.json'
g_LINE_PROB = None
# ENCODING = 'utf-8'
# ENCODING1 = 'gb18030'
# def dec(aStr):
#     gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
#     text, length = gb18030_decode(aStr, 'replace')
#     return text
# def enc(aStr):
#     gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
#     text, length = gb18030_encode(aStr, 'replace')
#     return text
# def dec1(aStr):
#     gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
#     text, length = gb18030_decode(aStr, 'replace')
#     return text
# def enc1(aStr):
#     gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
#     text, length = gb18030_encode(aStr, 'replace')
#     return text

class BBNPlus(BBN):
    def __init__(self, nodes_dict, name=None, domains={}):
        BBN.__init__(self, nodes_dict, name=None, domains={})
    def get_graphviz_source_plus(self, dpi=200, rankdir='LL'):
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
    # client = pymongo.MongoClient('localhost', 27017)
    db = client['kmgd']
    if not collection in db.collection_names(False):
        ret = db.create_collection(collection)
    else:
        ret = db[collection]
    return ret

def get_state_examination_data_by_line_name(line_name, check_year_list = []):
    ret = []
    collection = get_collection('state_examination')
    if len(check_year_list)>0:
        ret = list(collection.find({'line_name':line_name, 'check_year':{'$in':check_year_list}}))
    else:
        ret = list(collection.find({'line_name':line_name}))
    return ret


def calc_probability1(data, field_name, field_value):
    def filterfunc(item):
        if not item.has_key(field_name):
            return False
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

def build_state_examination_condition(line_name):
    # data = get_state_examination_data_by_line_name(line_name)
    cond = {}
    # o = calc_probability_unit(data)
    # for k in o.keys():
    #     cond[k] = o[k]
    cond['line_state'] = []
    # o1 = calc_probability_line1()
    # cond['line_state'].extend(o1['line_state'])
    o = calc_probability_line()
    cond['line_state'].extend(o['line_state'])
    return cond

def build_additional_condition(line_name, cond):
    ret = cond
    collection = get_collection('bayesian_nodes')
    l = list(collection.find({'line_name':line_name}))
    for node in l:
        # name = node['name']
        # domains = node['domains']
        ret[node['name']] = node['conditions']
    return ret

def create_bbn_by_line_name(line_name):
    cond = build_state_examination_condition(line_name)
    cond = build_additional_condition(line_name, cond)
    g = None
    if USE_C_MODULE:
        print('using c-accelerate module...')
        g = build_bbn_from_conditionals(cond)
    else:
        print('using pure-python module...')
        g = build_bbn_from_conditionals_plus(cond)
    return g

# def _create_bbn_by_line_name(line_name):
#     cond = build_state_examination_condition(line_name)
#     cond = build_additional_condition(line_name, cond)
#     g = build_bbn_from_conditionals(cond)
#     return g

def build_additional_condition_fake(cond):
    ret = cond
    for i in range(1, 9):
        ret['unit_%d' % i] = [
            [[],{
                'I': 0.0,
                'II': 0.0,
                'III': 0.0,
                'IV': 0.0,
            }]
        ]
    return ret

def query_bbn_condition(g, **querydict):
    print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'start'))
    d = g.query(**querydict)
    print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'end'))
    ret = []
    for k, v in d.iteritems():
        # if v < 1.0 and v > 0.0:
        # if v > 0.0:
        o = {}
        # o['%s:%s' % (k[0], k[1])] = v
        o['name'] = k[0]
        o['value'] = k[1]
        o['p'] = v
        ret.append(o)
    return ret


def test_se():
    if USE_C_MODULE:
        g = create_bbn_by_line_name(u'厂口七甸I回线')
        print(g.get_graphviz_source())
        print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'q start'))
        # g.q(line_state='II')
        ret = query_bbn_condition(g,  line_state='II')
        print (ret)
        print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'q end'))
    else:
        g = create_bbn_by_line_name(u'厂口七甸I回线')
        print(g.get_graphviz_source_plus())
        print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'q start'))
        # g.q(line_state='II')
        ret = query_bbn_condition(g, line_state='II')
        print (ret)
        print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'q end'))
    # fg = build_graph_from_conditionals_plus(cond)
    # print(fg.export_plus(None))


def test_find_abnormal():
    collection = get_collection('state_examination')
    ids = []
    for i in list(collection.find({})):
        for j in range(1, 9):
            if i.has_key('unit_%d' % j):
                if ' ' in i['unit_%d' % j]:
                    print('%s:%d' % (enc1(i['line_name']), i['check_year']))
        if i.has_key('line_state' ):
            if ' ' in i['line_state']:
                print('line_state%s:%d' % (enc1(i['line_name']), i['check_year']))
        if '-' in i['line_name']:
            print('%s:%d' % (enc1(i['line_name']), i['check_year']))
            ids.append(i['_id'])
        if not i['line_name'][-1] == u'线':
            print('%s:%d' % (enc1(i['line_name']), i['check_year']))
            ids.append(i['_id'])

    # collection.remove({'_id':{'$in':ids}})




def test_bayes():
    cond = build_cancer_condition()
    g = build_bbn_from_conditionals(cond)
    test(g)
    # g = build_bbn_plus(
    #     fP, fS, fC, fX, fD,
    #     domains={
    #         'P': ['low', 'high']})
    print(g.get_graphviz_source())
    fg = build_graph_from_conditionals_plus(cond)
    # fg = build_graph_plus(
    #     fP, fS, fC, fX, fD,
    #     domains={
    #         'P': ['low', 'high']})
    print(fg.export_plus(None))
    # # g.q()
    # g.q(P='high')
    # g.q(D=True)
    # # g.q(S=True)
    # # g.q(C=True, S=True)
    # # g.q(D=True, S=True)
    # # print(g.factor_nodes())
    # # print(fg.export(None))


    # print(g.get_graphviz_source())
    # g.q()

# def calc_probability_line():
#     retname, retlist = 'line_state', []
#     ret = {}
#     l = []
#     for i in range(8):
#         l.append(['1', '2', '3', '4'])
#     iterator = itertools.product(*l)
#     total = 0
#     total_map = {}
#
#     for it in iterator:
#         for i in range(1, 5):
#             if get_max_level(it) == i:
#                 if not total_map.has_key(str(i)):
#                     total_map[str(i)] = 0
#                 total_map[str(i)] += 1
#         total += 1
#     o = {}
#     for i in range(1, 5):
#         p = float(total_map[str(i)])/float(total)
#         o[get_level_name(i)] = p
#         print('%f' % p)
#
#     retlist.append([[], o])
#     ret[retname] = retlist
#     return ret

def get_max_level(alist):
    l = [int(i) for i in alist]
    return max(l)
def check_is_equal(alist, *args):
    ret = True
    for i in args:
        if isinstance(i, dict):
            ret = ret and (alist[i['unit_index']-1] == i['unit_level'])
        else:
            raise Exception('args must be tuple of dict')
    return ret
def get_level_name(idx):
    if isinstance(idx, str) or isinstance(idx, unicode):
        idx = int(idx)
    ret = ''
    if idx == 1:
        ret = 'I'
    if idx == 2:
        ret = 'II'
    if idx == 3:
        ret = 'III'
    if idx == 4:
        ret = 'IV'
    return ret


def calc_probability_unit(data):
    ret = {}
    for i in range(1, 9):
        ret['unit_%d' % i] = [
            [[],{
                'I':  calc_probability1(data, 'unit_%d' % i, 'I'),
                'II': calc_probability1(data, 'unit_%d' % i, 'II'),
                'III':calc_probability1(data, 'unit_%d' % i, 'III'),
                'IV': calc_probability1(data, 'unit_%d' % i, 'IV'),
                 }
             ]
        ]
    return ret


def calc_probability_line():
    global  g_LINE_PROB
    ret = {}
    if g_LINE_PROB:
        ret = g_LINE_PROB
    elif os.path.exists(P_LINE_UNIT_PATH):
        with open(P_LINE_UNIT_PATH) as f:
            ret = json.load(f)
            g_LINE_PROB = ret
    else:
        l = []
        for i in range(8):
            l.append(['1', '2', '3', '4'])
        iterator = itertools.product(*l)
        total = 0
        total_map = {}
        list1 = []
        for it in iterator:
            max_line_level = get_max_level(it)
            list2 = []
            list3 = []
            idx = 0
            for i in it:
                list3.append(['unit_%d' % (idx+1), get_level_name(i)])
                idx += 1
            list2.append(list3)
            o = {}
            for i in range(1, 5):
                o[get_level_name(i)] = 0.0
            o[get_level_name(max_line_level)] = 1.0
            list2.append(o)
            list1.append(list2)
            total += 1
        ret['line_state'] = list1
        g_LINE_PROB = ret
        with open(P_LINE_UNIT_PATH, 'w') as f:
            json.dump(ret, f, ensure_ascii=True)
    return ret

def calc_probability_line1():
    ret = {}
    if os.path.exists(P_LINE_UNIT_PATH1):
        print(u'existing probability file [%s], reading...' % P_LINE_UNIT_PATH1)
        with open(P_LINE_UNIT_PATH1) as f:
            ret = json.load(f)
    else:
        print(u'not found probability file, generating...')
        l = []
        for i in range(8):
            l.append(['1', '2', '3', '4'])
        iterator = itertools.product(*l)
        total = 0
        total_map = {}
        for it in iterator:
            max_lev = get_max_level(it)
            # for line_lev in range(1, 5):
            #     if max_lev == line_lev:
            #         key_line = 'line:%d' % line_lev
            #         if not total_map.has_key(key_line):
            #             total_map[key_line] = 0
            #         total_map[key_line] += 1
            #         break
            unit_lev = int(it[0])
            if unit_lev <= max_lev:
                key_line_unit = 'line:%d|unit:%d' % (max_lev,  unit_lev)
                if not total_map.has_key(key_line_unit):
                    total_map[key_line_unit] = 0
                total_map[key_line_unit] += 1
            total += 1
        # p_line = {}
        p_line_unit = {}
        for i in range(1, 5):
            key_unit = 'unit:%d' % i
            total_map[key_unit] = pow(4, 7)
            for j in range(1, 5):
                key_line_unit = 'line:%d|unit:%d' % (i,  j)
                if total_map.has_key(key_line_unit):
                    p_line_unit[key_line_unit] = float(total_map[key_line_unit])/float(total_map[key_unit])
                else:
                    p_line_unit[key_line_unit] = 0.0



        # for i in range(1, 5):
        #     # p = float(total_map[str(i)])/float(total)
        #     key_line = 'line:%d' % i
        #     p = float(total_map[key_line])/float(total)
        #     p_line[get_level_name(i)] = p

        ret['line_state'] = []
        for unit_idx in range(1, 9):
            for unit_lev in range(1, 5):
                list1 = []
                list1.append([['unit_%d' % unit_idx, get_level_name(unit_lev)],])
                o = {}
                for line_lev in range(1, 5):
                    key_line_unit = 'line:%d|unit:%d' % (line_lev,  unit_lev)
                    o[get_level_name(line_lev)] = p_line_unit[key_line_unit]
                list1.append(o)
                ret['line_state'].append(list1)

        with open(P_LINE_UNIT_PATH1, 'w') as f:
            json.dump(ret, f, ensure_ascii=True)
        # with codecs.open(P_LINE_UNIT_PATH1, 'w', 'utf-8-sig') as f:
        #     f.write(json.dumps(ret, ensure_ascii=False, indent=4))
    return ret



def get_all_combinations(max_num):
    def filter_func(item):
        ret = False
        if len(item) == 1:
            ret = True
        elif len(item) > 1:
            names = []
            for i in item:
                if i[0] in names:
                    ret = False
                    break
                else:
                    names.append(i[0])
            if len(item) == len(names):
                ret = True
        return ret
    ret = []
    p = list(itertools.product(['1','2','3','4','5','6','7','8'], ['1', '2', '3', '4']))
    for i in range(1, max_num+1):
        list1 = []
        for j in itertools.combinations(p, i):
            if filter_func(j):
                list1.append(j)
        ret.extend(list1)
        # print('%d:%d' % (i, len(ret)))
    return ret

def test_aggregation():
    collection = get_collection('state_examination')
    pipeline = [
        # {'$unwind':'$line_name'},
        {"$group": {"_id": "$line_name", "count": {"$sum": 1}}},
    ]
    ret = list(collection.aggregate(pipeline))
    ret = map(lambda x:x['_id'], ret)
    print(ret)

def test_import_unit_probability_map_reduce():
    collection = get_collection('state_examination')
    mapfunc = Code("function() {"
              "   emit(this.line_name, {line_state:this.line_state});"
              "}"
              )

    reducefunc = Code("function(key,values){"
                  "    var result={I:0, II:0, III:0, IV:0, total:0};"
                  "    for (var i = 0; i < values.length; i++) {"
                  "       if(values[i].line_state === 'I')"
                  "            result.I += 1;"
                  "       if(values[i].line_state === 'II')"
                  "            result.II += 1;"
                  "       if(values[i].line_state === 'III')"
                  "            result.III += 1;"
                  "       if(values[i].line_state === 'IV')"
                  "            result.IV += 1;"
                  "       result.total += 1;"
                  "    }"
                  "    return result;"
                  "}"
                 )
    finalizefunc = Code("function(key,values){"
                  "   var result={I_probability:0.0, II_probability:0.0, III_probability:0.0, IV_probability:0.0};"
                  "   result.I_probability = values.I/values.total;"
                  "   result.II_probability = values.II/values.total;"
                  "   result.III_probability = values.III/values.total;"
                  "   result.IV_probability = values.IV/values.total;"
                  "   return result;"
                  "}"
                 )
    results = collection.map_reduce(mapfunc,reducefunc, 'tmp', finalize=finalizefunc)
    print(results)

def test_trim_name():
    collection = get_collection('state_examination')
    for i in list(collection.find({})):
        i['line_name'] = i['line_name'].strip()
        collection.save(i)

def test_regenarate_unit():
    client = pymongo.MongoClient('192.168.1.8', 27017)
    db = client['kmgd']
    generate_unit_probability(db)

def generate_unit_probability(db):
    def get_domains(alist):
        d = OrderedDict(alist[0][1])
        return d.keys()

    def get_desc(alist, name):
        ret = []
        for i in alist:
            if i['parent'] == name:
                ret.append(i['name'])
        return ';\n'.join(ret)

    # client = pymongo.MongoClient('192.168.1.8', 27017)
    # db = client['kmgd']
    if 'bayesian_nodes' in db.collection_names(False):
        db.drop_collection('bayesian_nodes')

    path = ur'jiakongztpj.json'
    std = None
    with open(path) as f:
        std = json.loads(f.read())
    collection = get_collection('state_examination')
    pipeline = [
        # {'$unwind':'$line_name'},
        {"$group": {"_id": "$line_name", "count": {"$sum": 1}}},
    ]
    lines = list(collection.aggregate(pipeline))
    linenames = map(lambda x:x['_id'], lines)
    i = 0
    l = []
    for line_name in linenames:
        data = get_state_examination_data_by_line_name(line_name)
        print('%s:%d' % (enc1(line_name), len(data) ) )
        o = calc_probability_unit(data)
        # print (o)
        for k in o.keys():
            o1 = {}
            o1['name'] = k
            o1['display_name'] = UNIT_NAME_MAPPING[k]
            o1['line_name'] = line_name
            o1['description'] = get_desc(std, UNIT_NAME_MAPPING[k])
            o1['conditions'] = o[k]
            o1['domains'] = get_domains(o[k])
            l.append(o1)
            i += 1
        # if i > 30:
        #     break
    # with codecs.open(ur'd:\aaa.json', 'w', 'utf-8-sig') as f:
    #     f.write(json.dumps(l, ensure_ascii=False, indent=4))
    collection = get_collection('bayesian_nodes')
    for i in l:
        collection.save(i)

    # print(o)



def test_import_2015txt():
    path = ur'D:\2014项目\贝叶斯\贝叶斯隐形故障系统状态评价数据(2010-2015)\输电管理所2015年第一次状态评价报告.txt'
    lines = []
    l = []
    with open(path) as f:
        idx = 0
        for line in f.readlines():
            # if idx < 8:
            #     idx += 1
            #     continue
            lines.append(line.strip())
            # idx += 1

    for i in range(0, len(lines), 12):
        o = {}
        # o['index'] = dec(lines[i+1])
        # print(enc1(dec(lines[i+3])))
        o['check_year'] = 2015
        o['line_state'] = dec(lines[i+2]).replace(u'严重',u'IV').replace(u'异常',u'III').replace(u'注意',u'II').replace(u'正常',u'I')
        o['line_name'] = dec(lines[i+3]).replace(u'500kV', '').replace(u'220kV', '').replace(u'110kV', '').replace(u'Ⅰ', 'I').replace(u'Ⅱ', 'II')
        if o['line_name'][-1] == u'回':
            o['line_name'] = o['line_name'].replace(u'回', u'回线')
        o['voltage'] = dec(lines[i+4])
        o['description'] = dec(lines[i+9])
        o['suggestion'] = dec(lines[i+11])
        l.append(o)
        # print(o)
        # if i>100:
        #     break
    print(len(l))
    with codecs.open(path+'.json', 'w', 'utf-8-sig' ) as f:
        f.write(json.dumps(l, ensure_ascii=False, indent=4))
    export_xls(l)

def export_xls(alist):
    path = ur'D:\2014项目\贝叶斯\贝叶斯隐形故障系统状态评价数据(2010-2015)\输电管理所2015年第一次.xls'
    book = xlwt.Workbook()
    sheet = book.add_sheet('Sheet1')
    sheet.write(0, 0, u'line_name')
    sheet.write(0, 1, u'voltage')
    sheet.write(0, 2, u'check_year')
    sheet.write(0, 3, u'description')
    sheet.write(0, 4, u'suggestion')
    sheet.write(0, 5, u'line_state')
    for i in range(1, 9):
        sheet.write(0, i + 6, u'unit_%d' % i)
    row = 1
    for i in alist:
        # print(enc1(i['line_name']))
        # print(row)
        sheet.write(row, 0, i['line_name'])
        sheet.write(row, 1, i['voltage'])
        sheet.write(row, 2, i['check_year'])
        sheet.write(row, 3, i['description'])
        sheet.write(row, 4, i['suggestion'])
        sheet.write(row, 5, i['line_state'])
        row += 1
    book.save(path)

def test_insert_domains_range():
    data =  [
        {'value':'true', 'name': u'真'},
        {'value':'false', 'name': u'假'},
        {'value':'I', 'name': u'I级'},
        {'value':'II', 'name': u'II级'},
        {'value':'III', 'name': u'III级'},
        {'value':'IV', 'name': u'IV级'},
        {'value':'high', 'name': u'高'},
        {'value':'low', 'name': u'低'},
        {'value':'medium', 'name': u'中'},
    ]
    client = pymongo.MongoClient('192.168.1.8', 27017)
    db = client['kmgd']
    if 'bayesian_domains_range' in db.collection_names(False):
        db.drop_collection('bayesian_domains_range')
    collection = get_collection('bayesian_domains_range')
    for i in data:
        collection.save(i)

def test_combinations():
    l = calc_probability_line1()['line_state']
    m = {}
    for i in l:
        key = '%s:%s' % (i[0][0][0], i[0][0][1])
        if not m.has_key(key):
            m[key] = i[1]
    print(m)
    # l = []
    # cnt = 0
    # for i in range(1, 9):
    #     iterator = itertools.combinations(range(1, 9), i)
    #     for it in iterator:
    #         l.append(it)
    #         cnt += pow(4, len(it))
    #         # print(it)
    # print (len(l))
    # print (cnt)

def test_format_json():
    l = []
    with codecs.open(ur'd:\768.json', 'r', 'utf-8-sig' ) as f:
        l = json.loads(f.read())
    with codecs.open(ur'd:\768_1.json', 'w', 'utf-8-sig' ) as f:
        f.write(json.dumps(l, ensure_ascii=False))

def base64_img():
    import base64
    DIR_ROOT = ur'F:\work\html\webgis\css\ligerui-skins\Aqua\images'
    d = {}
    names = [
        'loading.gif',
        'popup-line.gif',
        'header-bg.gif',
        'bar-bg.gif',
        'icon-first.gif',
        'icon-prev.gif',
        'icon-next.gif',
        'icon-last.gif',
        'icon-load.gif',
        'bar-button-over.gif',
    ]
    for root, dirs, files  in os.walk(DIR_ROOT, topdown=False):
        for name in files:
            ext = name[name.rindex('.'):]
            if ext == '.%s' % 'gif':
                p = os.path.join(root, name)
                if name  in names:
                    print('converting to base64: %s ...' % p)
                    with open(p, 'rb') as f:
                        d[name] = base64.encodestring(f.read())
                        print(d[name])
    with open(ur'd:\aaa.json', 'w') as f:
        f.write(json.dumps(d, ensure_ascii=True, indent=4))

def cartesian_product(arrays):
    broadcastable = np.ix_(*arrays)
    broadcasted = np.broadcast_arrays(*broadcastable)
    rows, cols = reduce(np.multiply, broadcasted[0].shape), len(broadcasted)
    out = np.empty(rows * cols, dtype=broadcasted[0].dtype)
    start, end = 0, rows
    for a in broadcasted:
        out[start:end] = a.reshape(-1)
        start, end = end, end + rows
    return out.reshape(cols, rows).T

def array3d_creation(alist, w, h):
    l = []
    for i in alist:
        l1 = []
        for j in i:
            l1.append({j[0]:j[1]})
        l.append(np.array(l1))
    # print(l)
    p = cartesian_product(l)
    ret = np.array((len(p), w, h), dtype=object)
    # print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'start'))
    # permutations = product(*l)
    # print(len(list(permutations)))
    # print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'end'))
    return ret

def test_numpy():
    w = 9
    h = 9

    arr = [[('line_state', u'I'), ('line_state', u'II'), ('line_state', u'III'), ('line_state', u'IV')], [(u'unit_1', u'I'), (u'unit_1', u'II'), (u'unit_1', u'III'), (u'unit_1', u'IV')], [(u'unit_2', u'I'), (u'unit_2', u'II'), (u'unit_2', u'III'), (u'unit_2', u'IV')], [(u'unit_3', u'I'), (u'unit_3', u'II'), (u'unit_3', u'III'), (u'unit_3', u'IV')], [(u'unit_4', u'I'), (u'unit_4', u'II'), (u'unit_4', u'III'), (u'unit_4', u'IV')], [(u'unit_5', u'I'), (u'unit_5', u'II'), (u'unit_5', u'III'), (u'unit_5', u'IV')], [(u'unit_6', u'I'), (u'unit_6', u'II'), (u'unit_6', u'III'), (u'unit_6', u'IV')], [(u'unit_7', u'I'), (u'unit_7', u'II'), (u'unit_7', u'III'), (u'unit_7', u'IV')], [(u'unit_8', u'I'), (u'unit_8', u'II'), (u'unit_8', u'III'), (u'unit_8', u'IV')]]
    a = array3d_creation(arr, w, h)


def test_get_pastyears_bbn_data():
    p = ur'd:\2010_2014.json'
    ret = []
    with codecs.open(p, 'r', 'utf-8-sig') as f:
        ret = json.loads(f.read())
    return ret

def test_get_st_by_year(line_name, year):
    collection = get_collection('state_examination')
    ret = list(collection.find({'line_name':line_name, 'check_year':year}))
    return ret

def test_compare_precision():
    data = test_get_pastyears_bbn_data()
    ok_count = 0
    total_count = 0
    for i in data:
        line_name = i['line_name']
        actual = test_get_st_by_year(line_name, 2015)
        line_state = ''
        unitkey = ''
        if len(actual)>0:
            line_state = actual[0]['line_state']
            print('%s' % line_name)
            print('    actual:2015')
            print('        line is state %s:' % line_state)
            ll = actual[0].keys()
            ll.sort()
            for k in ll:
                if not  k in ['_id', 'line_id', 'voltage', 'line_state', 'line_name', 'check_year','description', 'suggestion' ]:
                     if actual[0][k] == line_state:
                        print('            %s: %s' % (k, actual[0][k]))
                        unitkey = '%s:%s' % (k, actual[0][k])
            print('    predict:%s' % str(i['check_year']))
            for j in [u'II', u'III', u'IV']:
                if j == line_state:
                    print('        line in state %s:' % j)
                    ll = i[j].keys()
                    ll.sort()
                    for k in ll:
                        if not 'line_state' in k:
                            if i[j][k]>0 and k == unitkey:
                                print('            %s: %.2f' % (k, i[j][k]))
                                ok_count += 1
            if 2014 in i['check_year']:
                total_count += 1
    print('total:%d, right:%d, percentage:%.2f' % (total_count, ok_count,  float(ok_count)/float(total_count)))


def test_calc_past_year(past_years_list=[]):
    def get_domains(alist):
        d = OrderedDict(alist[0][1])
        return d.keys()
    def convert_tuple(adict):
        ret = {}
        for k in adict.keys():
            key = ':'.join([k[0], k[1]])
            ret[key] = adict[k]
        return ret
    collection = get_collection('state_examination')
    pipeline = [
        # {'$unwind':'$line_name'},
        {"$group": {"_id": "$line_name", "count": {"$sum": 1}}},
    ]
    lines = list(collection.aggregate(pipeline))
    linenames = map(lambda x:x['_id'], lines)
    i = 0
    ret = []
    for line_name in linenames:
        l = []
        result = {}
        data = get_state_examination_data_by_line_name(line_name, past_years_list)
        check_year = []
        for i in data:
            check_year.append(i['check_year'])
        print('%s:%d:%s' % (enc1(line_name), len(data), str(check_year) ) )
        if len(check_year)>1:
            o = calc_probability_unit(data)
            result['line_name'] = line_name
            result['check_year'] = check_year
            for k in o.keys():
                o1 = {}
                o1['name'] = k
                # o1['display_name'] = UNIT_NAME_MAPPING[k]
                # o1['line_name'] = line_name
                o1['conditions'] = o[k]
                o1['domains'] = get_domains(o[k])
                l.append(o1)
            cond = {}
            cond['line_state'] = []
            o = calc_probability_line()
            cond['line_state'].extend(o['line_state'])
            for node in l:
                # name = node['name']
                # domains = node['domains']
                cond[node['name']] = node['conditions']
            g = build_bbn_from_conditionals(cond)
            result['II'] =  convert_tuple(g.query(line_state = 'II'))
            result['III'] =  convert_tuple(g.query(line_state = 'III'))
            result['IV'] =  convert_tuple(g.query(line_state = 'IV'))
            ret.append(result)
            # break
        else:
            print('need 2 years or more')

    with codecs.open(ur'd:\2010_2014.json', 'w', 'utf-8-sig') as f:
        f.write(json.dumps(ret, ensure_ascii=False, indent=4))




if __name__ == '__main__':
    pass
    # test_regenarate_unit()
    # test_insert_domains_range()
    # test_import_2015txt()
    # test_se()
    # reset_unit_by_line_name(u'厂口七甸I回线')
    # test_numpy()
    # test_format_json()
    # base64_img()
    # test_combinations()
    # calc_probability_line1()
    # test_find_abnormal()
    # test_aggregation()
    # test_trim_name()
    # test_import_unit_probability_map_reduce()
    # test_import_unit_probability()
    # test_bayes()
    # test_calc_past_year(range(2010, 2015))
    # test_compare_precision()





