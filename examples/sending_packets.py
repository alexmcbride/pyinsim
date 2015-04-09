"""Example 2: Same as example 1, except we create and send an actualy MST packet."""

import pyinsim

# Init new InSim object.
insim = pyinsim.insim('127.0.0.1', 29999, Admin='')

# Send an MST packet with the message 'Hello, InSim!' to the game.
insim.send(pyinsim.ISP_MST, Msg='Hello, InSim!')

# Start pyinsim.
pyinsim.run()
