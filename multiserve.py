"""
evoke mutli-app server script, for Twisted 
"""

#fix the path
import os, sys
sys.path.append(
    os.path.abspath('.'))  #some servers need this for some reason...
sys.path.append(os.path.abspath('..'))

from twisted.application import service
from evoke.serve import start
from config_multi import apps

## Twisted requires the creation of the root-level application object to take place in this file
application = service.Application("evoke application")
## stitch it all together...
start(application, apps)
