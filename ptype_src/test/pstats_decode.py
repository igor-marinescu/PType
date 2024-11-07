""" pstats Time extended function """

import pstats
from pstats import SortKey

def f_8(val):
    """ Modify time to show in us precision. """
    ret = "%8.3f" % val
    if ret != '   0.000':
        return ret
    return "%6dµs" % (val * 1000000)

pstats.f8 = f_8

p = pstats.Stats('profile.out')

#p.strip_dirs().sort_stats(SortKey.NAME).print_stats()
p.strip_dirs().sort_stats(SortKey.FILENAME).print_stats('backtiles')
