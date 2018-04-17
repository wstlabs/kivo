from ..util.csvarg import make_csv_args

def make_refresh_command(matview,concurrent=True):
    return f'refresh materialized view {matview};'


"""
_valid_delim = set([',','|'])
def is_valid_delim(c):
    return c in _valid_delim

def delim_term(c):
    if not is_valid_delim(c):
        raise ValueError("invalid delimiter [%s]" % c)
    return '\\"'+c+'\\"'

def make_csv_args(c):
    delimstr = '' if c == ',' else "DELIMETER %s, " % delim_term(c)
    return '('+delimstr+'FORMAT CSV, HEADER TRUE)' 
"""
