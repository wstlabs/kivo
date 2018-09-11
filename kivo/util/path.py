import os


"""
splitfull('/foo/bar/baz')
['/', 'foo', 'bar', 'baz']
>>> splitfull('/foo')
['/', 'foo']
>>> splitfull('/')
['/']
>>> splitfull('')
[]
"""

def splitfull(path):
    """Splits a filepath into constituent terms, compatible with the behavior of os.path.split"""
    terms = []
    while path != '':
        head,tail = os.path.split(path)
        if (head,tail) == ('/',''):
            head,tail = '','/'
        terms += [tail]
        path = head
    return list(reversed(terms))

