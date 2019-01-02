import re
from collections import OrderedDict

_validtempos = ('yearly','monthly','daily','regular','sporadic')

_pairs = [('special',5),('refine',4),('extract',3),('unpack',2),('incoming',1),('proto',0)]
_label2index = OrderedDict(_pairs)
_index2label = OrderedDict((v,k) for k,v in _pairs)
_validlabels = list(reversed(_label2index.keys()))

def label2index(label):
    return _label2index.get(label)

def index2label(index):
    return _index2label.get(index)

def is_valid_label(label):
    return label in _label2index

def is_valid_index(index):
    return index in _index2label

def is_valid_tempo(tempo):
    return tempo in _validtempos

def is_valid_source(source):
    return is_dashy(source)

def is_valid_version(version):
    return is_dashy(version)

def valid_labels():
    return list(_validlabels)

def valid_tempos():
    return list(_validtempos)

def phasetup(index=None,label=None):
    if index is not None and label is not None:
        raise ValueError("index and label arguments are mutually exclusive")
    if index is not None:
        label = index2label(index)
        if label is None:
            raise ValueError(f"invalid index '{index}'")
        return index,label
    if label is not None:
        index = label2index(label)
        if index is None:
            raise ValueError(f"invalid label '{label}'")
        return index,label
    raise ValueError("exactly one of index or label arguments must be supplied")

def phasedir(index=None,label=None):
    _index,_label = phasetup(index,label)
    return f'{_index}-{_label}'

# XXX description needed
_dashypat = re.compile('^[a-z0-9][a-z0-9\-]*[a-z0-9]*$')
def is_dashy(s):
    if not isinstance(s,str):
        return False
    return re.match(_dashypat,s)

_extpat = re.compile('^[A-Za-z0-9]+$')
def is_ext(s):
    """
    Returns true if this appears to be a valid file extension, e.g. 'csv', 'mp3', etc.
    """
    if not isinstance(s,str):
        return False
    return re.match(_extpat,s)

