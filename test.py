"""Example 1: Initialize InSim and send the message 'Hello, InSim!' to the chat."""

import pyinsim

def init(insim):
    print ('InSim initialized')

def closed(insim):
    print('InSim connection closed')

def error(insim):
    print('InSim error:')
    import traceback
    traceback.print_exc()

def all(insim, packet):
    print(vars(packet))

# Initialize the InSim system
insim = pyinsim.insim('127.0.0.1', 29999, Admin=b'', ReqI=1)

# Send message 'Hello, InSim!' to the game
insim.sendm(b'/msg Hello')


insim.bind(pyinsim.EVT_INIT, init)
insim.bind(pyinsim.EVT_CLOSE, closed)
insim.bind(pyinsim.EVT_ERROR, error)
insim.bind(pyinsim.EVT_ALL, all)

# Start pyinsim.
pyinsim.run()

