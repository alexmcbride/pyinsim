"Example: Shows how to use InSim relay to select a single host."

import pyinsim

# Replace with host name
HOST_NAME = 'RallyX Layout Bw'

def autstr(ob):
    """AutoString 
    Automatically converts bytes to string if it has to
    """
    return ob.decode() if type(ob)==bytes else ob

def new_connection(relay, ncn):
    # Print out connection name.
    print( 'New Connection:', autstr(ncn.UName))

# Initialize relay host.
relay = pyinsim.relay(HName=HOST_NAME)

# Bind events.
relay.bind(pyinsim.ISP_NCN, new_connection)

# Request connection list from host.
relay.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NCN)

# Run pyinsim.
pyinsim.run()
