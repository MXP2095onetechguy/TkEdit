# Set the version of Pmw to use for the demonstrations based on the
# directory name.

import importlib
import os
import string

def expandLinks(path):
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    while 1:
        if not os.path.islink(path):
            break
        dir = os.path.dirname(path)
        path = os.path.join(dir, os.readlink(path))

    return path

def setPmwVersion():
    file = importlib.util.find_spec(__name__).origin
    file = os.path.normpath(file)
    file = expandLinks(file)

    dir = os.path.dirname(file)
    dir = expandLinks(dir)
    dir = os.path.dirname(dir)
    dir = expandLinks(dir)
    dir = os.path.basename(dir)

    version = dir[4:].replace('_', '.')
    import Pmw
    if version in Pmw.installedversions():
        Pmw.setversion(version)
    else:
        print('No such Pmw version ' + str(version) + '.')
        print('Using default version ' + str(Pmw.version()))
