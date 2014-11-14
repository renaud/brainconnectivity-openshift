import csv, re
from collections import defaultdict


'''load ABA "ontology", incl mapping to new my_ids'''
_onto = {}     # k: br_name, v: aba_id
_name = {}     # k: aba_id,  v: br_name
_abbrev = {}   # k: aba_id,  v: abbreviation
_mapping = {}  # k: aba_id,  v: my_id
_parent = {}   # k: aba_id,  v: parent_id
_children = {} # k: aba_id,  v: list of children ids
def load_aba_onto():
    with open('data/ABA.tsv') as tsv:
        next(tsv)
        for line in csv.reader(tsv, delimiter='\t'):
            aba_id  =    int(line[0])
            my_id   =    int(line[1])
            abbrev   =        line[3]
            br_name =        line[4]
            _onto[br_name]   = aba_id
            _name[aba_id]    = br_name
            _abbrev[aba_id]   = abbrev
            _mapping[aba_id] = my_id
            if (not line[5] == 'null'): #not root
                parent_id =  int(line[5])
                _parent[aba_id] = parent_id
                if (parent_id not in _children):
                    _children[parent_id] = []
                _children[parent_id].append(aba_id)
    print 'ABA loaded with {} items.'.format(len(_onto))
load_aba_onto()
assert _onto['intraparafloccular fissure'] == 49, 'could not load aba onto'
assert _mapping[49] == 44, 'could not load aba onto'


def ids():
    return list(_name.keys())
assert 262 in ids()


def name(aba_id):
    return _name[aba_id]
assert name(343) == 'Brain stem'


def abbrev(aba_id):
    return _abbrev[aba_id]
assert abbrev(343) == 'BS'


def parent(aba_id):
    return _parent[aba_id]
assert parent(343) == 8, 'Brain stem parent'


# recursive, so might be a bit slow
def parents(aba_id):
    if (aba_id not in _parent): # no parent anymore
        return []
    else:
        return [_parent[aba_id]] + parents(_parent[aba_id])
assert parents(343) == [8, 997], 'Brain stem parents'
assert parents(997) == [], 'root has no parents'


'''The direct children of this node'''
def children(aba_id):
    if (aba_id not in _children): # no children
        return []
    else:
        return list(_children[aba_id]) # return a copy!
assert children(385) == [33, 305, 593, 721, 778, 821]


def is_leaf(aba_id):
    return not (aba_id in _children)
assert not is_leaf(997), 'root is not a leaf'
assert is_leaf(18), 'nodular fissure is leaf'


def leaves():
    for id in _mapping.keys():
        if is_leaf(id):
            yield id
#for l in leaves():    print l

def branches():
    for id in _mapping.keys():
        if not is_leaf(id):
            yield id


'''All children of this node'''
def descendants(aba_id, only_leaves=False):
    if not children(aba_id): # no children
        return []
    else:
        ret = children(aba_id)
        if only_leaves:
            ret = filter(is_leaf, ret)
        for child in children(aba_id):
            ret += descendants(child)
        return ret
assert descendants(385) == [33, 305, 593, 721, 778, 821]
assert len(descendants(669)) == 48
assert len(descendants(669)) == 48
assert len(descendants(375)) > len(descendants(375, True))


def is_child(parent, child):
    return child in children(parent)
assert is_child(385, 593)


def is_parent(child, parent):
    return is_child(parent, child)
assert is_parent(343, 8), 'grey is parent of Brain stem'


def depth(aba_id):
    return len(parents(aba_id))
assert depth(997) == 0, 'root has depth 0'
assert depth(343) == 2, 'Brain stem has depth 2'


def height(aba_id):
    _height = 0
    for child in children(aba_id):
        _height = max(_height, height(child) + 1)
    return _height
assert height(385) == 1, 'height error'
assert height(669) == 2, 'height error'


''' @return br_ids that do NOT contain words like ", layer X" or ", XX part"'''
def filtered_ids():
    for br_name, aba_id in _onto.items():
        if not re.search(r'(, [lL]ayer|part)', br_name):
            yield aba_id
#for fid in filtered_ids():    print fid
