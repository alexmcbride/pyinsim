"""Example 1: Initialize InSim and send the message 'Hello, InSim!' to the chat."""

import pyinsim

# Initialize the InSim system #The IP and Port are to be found in the options when hosting a server
insim = pyinsim.insim('127.0.0.1', 58672, Admin='YourAdminPassword')

# Send message 'Hello, InSim!' to the game
insim.sendm('Hello, InSim!')

# Start pyinsim.
pyinsim.run()
