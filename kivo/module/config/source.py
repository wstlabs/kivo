import os
from collections import OrderedDict
from copy import deepcopy
from ...logging import log
import yaml

DEFAULTS = {'active':True}

def load(modpath):
    log.debug(f'modpath = {modpath}')
    cfgpath = f'{modpath}/source.yaml'
    if not os.path.exists(cfgpath):
        raise ValueError("invalid module directory (no 'source.yaml') found")
    blocks = _load_yaml(cfgpath)
    return process(blocks)

def process(blocks):
    newcfg = {'prefix':OrderedDict()}
    for block in blocks:
        process_block(newcfg,block)
    return newcfg

def process_block(newcfg,block):
    log.debug(f'newcfg = {newcfg}')
    prefix = deepcopy(block['meta']['prefix'])
    family = deepcopy(block['meta']['family'])
    assert isinstance(prefix,str)
    assert isinstance(family,str)
    if prefix not in newcfg['prefix']:
        newcfg['prefix'][prefix] = OrderedDict()
    t = newcfg['prefix'][prefix]
    for table in block['tables']:
        log.debug(f'table = {table}')
        r = deepcopy(table)
        name = r['name']
        del r['name']
        r['family'] = family
        t[name] = r

def _load_yaml(path):
    with open(path,"rtU") as f:
        return yaml.load(f)

def augment(r,d):
    """Creats a new dict which is a deepcopy of r, overlayed with values from d."""
    rr = deepcopy(r)
    for k,v in d.items():
        if k not in rr:
            rr[k] = deepcopy(v)
    return rr


#
# DEPRECATED
#

def __process(blocks):
    cfg = blocks[0]
    table_recs_raw = cfg['tables']
    table_recs_aug = [augment(r,DEFAULTS) for r in table_recs_raw]
    cfg['tables'] = recs2dict(table_recs_aug)
    return cfg

def __splitpath(srcpath):
    if isinstance(srcpath,str):
        terms = srcpath.split('.')
        if len(terms) == 1:
            return terms[0],None
        if len(terms) == 2:
            return tuple(terms)
    raise ValueError("invalid source path [%s]" % srcpath)

def __tablename(schema,prefix,name):
    _prefix = prefix.replace('-','_')
    _name = name.replace('-','_')
    return "%s.%s_%s" % (schema,_prefix,_name)

def __source2prefix(srcpath):
    terms = srcpath.split('.')
    if len(terms) > 1:
        return terms[0]
    raise ValueError("invalid source path [%s]" % srcpath)

def __recs2dict(recs):
    d = OrderedDict()
    for r in recs:
        name = r['name']
        del r['name']
        if name in d:
            raise ValueError("invalid configuration - duplicated source name '%s' detected" % name)
        d[name] = deepcopy(r)
    return d


