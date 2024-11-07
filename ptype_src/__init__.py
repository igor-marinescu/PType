""" PType Module __init__  """
import sys
import os

from . import ptype
from .test import test_backtiles
from .test import test_plates
from .test import test_anim

TEST = None
#TEST = 'ANIM'
#TEST = 'BACKTILES'
#TEST = 'PLATES'

def _real_main(argv=None):
    """ Real main function, invoke the desired module """
    #print('__init__._real_main()')

    # get the path + filename
    # Example: C:\Users\...\RubikQuat\rubikquat_src\__init__.pyc
    path = os.path.realpath(os.path.abspath(__file__))
    # remove filename (leave only path)
    # Example: C:\Users\...\RubikQuat\rubikquat_src
    path = os.path.dirname(path)

    # if frozen (py2exe generated exe) remove the 'rubikquat.exe'
    # from: C:\Users\...\RubikQuat\build\rubikquat.exe\rubikquat_src
    #   to: C:\Users\...\RubikQuat\build\
    if hasattr(sys, 'frozen'):
        path = os.path.dirname(path)
        path = os.path.dirname(path)

    if TEST == 'BACKTILES':
        module = test_backtiles.TestBacktiles(600, 600, path)
    elif TEST == 'PLATES':
        module = test_plates.TestPlates(600, 600, path)
    elif TEST == 'ANIM':
        module = test_anim.TestAnim(600, 600, path)
    else:
        module = ptype.PType(600, 600, path)
    module.run()

    retcode = 0
    sys.exit(retcode)


def main(argv=None):
    """ Main Function """
    #print('__init__.main()')
    _real_main(argv)
