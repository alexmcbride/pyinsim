"""Example 4: Bind pyinsim top-level events."""

import pyinsim

def init(insim):
    print('InSim initialized')
    
def closed(insim):
    print('InSim connection closed')
    
def error(insim):
    print('InSim error:')
    import traceback
    traceback.print_exc()

def all(insim, packet):
    print(vars(packet))

insim = pyinsim.insim('127.0.0.1', 58672, Admin='YourAdminPassword')

insim.bind(pyinsim.EVT_INIT, init)
insim.bind(pyinsim.EVT_CLOSE, closed)
insim.bind(pyinsim.EVT_ERROR, error)
insim.bind(pyinsim.EVT_ALL, all)

pyinsim.run()
