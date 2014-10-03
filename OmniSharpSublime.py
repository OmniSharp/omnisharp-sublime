# TODO: Omnisharp server가 sublime이 꺼지면 같이 꺼져야함.
import sys

from .listeners import *
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('OmniSharpSublime works with Sublime Text 3 only')


def plugin_loaded():
    print('omnisharp plugin_loaded')


def plugin_unloaded():
    print('omnisharp plugin_unloaded')
