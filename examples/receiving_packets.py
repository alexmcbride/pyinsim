"""Example 3: Bind a handler for the MSO packet event."""

import pyinsim

def message_out(insim, mso):
    # Print out the MSO message.
    print mso.Msg

# Init new InSim object.
insim = pyinsim.insim('127.0.0.1', 29999, Admin='')

# Bind packet called for the MSO packet.
insim.bind(pyinsim.ISP_MSO, message_out)

# Start pyinsim.
pyinsim.run()
