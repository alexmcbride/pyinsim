import pyinsim

# Store the connection and player lists in dictionaries.
connections = {}
players = {}


def new_connection(insim, ncn):
    # Add a new connection to the connections dict.
    connections[ncn.UCID] = ncn
    print 'New connection: %s' % ncn.UName
    
    
def connection_left(insim, cnl):
    # Get connection from connections dict.
    ncn = connections[cnl.UCID]
    # Delete the connection from the dict.
    del connections[cnl.UCID]
    print 'Connection left: %s' % ncn.UName
    
    
def new_player(insim, npl):
    # Add the new player to the players dict.
    players[npl.PLID] = npl
    print 'New player: %s' % pyinsim.stripcols(npl.PName)
    
    
def player_left(insim, pll):
    # Get player from the players dict.
    npl = players[pll.PLID]
    # Delete them from the dict.
    del players[pll.PLID]
    print 'Player left: %s' % pyinsim.stripcols(npl.PName)
    

# Init new InSim object.
insim = pyinsim.insim('127.0.0.1', 29999, Admin='')

# Bind events for the connection and player packets.
insim.bind(pyinsim.ISP_NCN, new_connection)
insim.bind(pyinsim.ISP_CNL, connection_left)
insim.bind(pyinsim.ISP_NPL, new_player)
insim.bind(pyinsim.ISP_PLL, player_left)

# Request for LFS to send all connections and players.
insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NCN)
insim.send(pyinsim.ISP_TINY, ReqI=255, SubT=pyinsim.TINY_NPL)

# Start pyinsim.
pyinsim.run()
