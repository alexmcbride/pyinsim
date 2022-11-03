"""Example 3: Bind a handler for the MSO packet event."""

import pyinsim

def autstr(ob):
    """AutoString 
    Automatically converts bytes to string if it has to
    """
    return ob.decode() if type(ob)==bytes else ob

def message_out(insim, mso):
    # Print out the MSO message.
    print(autstr(mso.Msg))

# Init new InSim object.
insim = pyinsim.insim('127.0.0.1', 58672, Admin='YourAdminPassword')

# Bind packet called for the MSO packet.
insim.bind(pyinsim.ISP_MSO, message_out)

# Start pyinsim.
pyinsim.run()
