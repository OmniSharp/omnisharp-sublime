import sys

from .listeners import *

if sys.version_info < (3, 3):
    raise RuntimeError('OmniSharpSublime works with Sublime Text 3 only')


def plugin_loaded():
    print('plugin_loaded')


def plugin_unloaded():
    print('plugin_unloaded')
