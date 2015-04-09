# __init__.py - init module for pyinsim
#
# Copyright 2008-2015 Alex McBride <xandermcbride@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 3 or any later version.
#

__version__ = '2.1.0'

from core import *
from insim import *
from func import *

__all__ = []
__all__.extend([c for c in dir(__import__('pyinsim.core'))])
__all__.extend([i for i in dir(__import__('pyinsim.insim'))])
__all__.extend([f for f in dir(__import__('pyinsim.func'))])
