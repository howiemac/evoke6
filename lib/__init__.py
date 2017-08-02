"""
evoke library interface


(IHM April 2007, 2017)
"""

#make everything visible as base.lib
from .library import * 
from ..types import *
from .deprecated import *
from .error import Error
from .permit import Permit, Condition
from .bug import send_error

