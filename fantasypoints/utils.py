import collections

def _numDigits(a):
    return len(str(a))

def _formatBlock(replacement=None, alignment=None, width=None, percision=None):
    block = '{'
    if replacement is not None:
        block += replacement
    block += ':'
    if alignment is not None:
        block += alignment
    if width is not None:
        block += str(width)
    if percision is not None:
        block += '.' + str(percision) + 'f'
    block += '}'
    return block

def _longestPlayerName(players):
    return len(str(max(players, key=lambda x:len(str(x)))))

def namedtuple_with_defaults(typename, field_names, default_values=()):
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T
