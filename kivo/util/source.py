import re
from collections import OrderedDict
from copy import deepcopy
from ..logging import log
import yaml


def split_table_spec(srcpath):
    # raise RuntimeError("deprecated")
    if isinstance(srcpath,str):
        terms = srcpath.split('.')
        if len(terms) == 1:
            return terms[0],None
        if len(terms) == 2:
            return tuple(terms)
    raise ValueError("invalid source path [%s]" % srcpath)

splitpath = split_table_spec

PAT = {}
PAT['tablespec'] = re.compile('^[\w\-]+$')
def is_valid_tablespec(tablespec):
    return bool(re.match(PAT['tablespec'],tablespec))

# def tablename(schema='public',prefix=None,name):
def tablename(schema='public',tablespec=None):
    assert is_valid_tablespec(tablespec)
    tablename = tablespec.replace('-','_')
    return "%s.%s" % (schema,tablename)

def __tablename(schema='public',prefix=None,name=None):
    _prefix = prefix.replace('-','_') if prefix else None
    _name = name.replace('-','_')
    return "%s.%s_%s" % (schema,_prefix,_name)

def source2prefix(srcpath):
    terms = srcpath.split('.')
    if len(terms) > 1:
        return terms[0]
    raise ValueError("invalid source path [%s]" % srcpath)


#
# DEPRECATED
#

__DEFAULTS = {'active':True}

def ___load_yaml(path):
    with open(path,"rtU") as f:
        return yaml.load(f)

def __augment(r,d):
    """Creats a new dict which is a deepcopy of r, overlayed with values from d."""
    rr = deepcopy(r)
    for k,v in d.items():
        if k not in rr:
            rr[k] = deepcopy(v)
    return rr

def ___load_and_augment(path):
    cfg = _load_yaml(path)[0]
    log.debug(f'cfg = {cfg}')
    table_recs_raw = cfg['tables']
    table_recs_aug = [augment(r,DEFAULTS) for r in table_recs_raw]
    cfg['tables'] = recs2dict(table_recs_aug)
    return cfg

def ___recs2dict(recs):
    d = OrderedDict()
    for r in recs:
        name = r['name']
        del r['name']
        if name in d:
            raise ValueError("invalid configuration - duplicated source name '%s' detected" % name)
        d[name] = deepcopy(r)
    return d

def __loadcfg_source(path):
    log.debug(f'path = {path}')
    cfg = load_and_augment(path)
    return cfg

