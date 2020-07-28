# core.py - core library module for pyinsim
#
# Copyright 2008-2020 Alex McBride <xandermcbride@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 3 or any later version.
#

# Dependencies
import socket
import asyncore
import traceback
import threading
import time

# Libraries
import pyinsim.insim as insim_

__all__ = [
    'EVT_ALL',
    'EVT_CLOSE',
    'EVT_ERROR',
    'EVT_INIT',
    'EVT_OUTGAUGE',
    'EVT_OUTSIM',
    'EVT_TIMEOUT',
    'INSIM_VERSION',
    'InSimError',
    'PYINSIM_VERSION',
    'closeall',
    'insim',
    'isrunning',
    'outgauge',
    'outsim',
    'packet',
    'relay',
    'run',
    'time',
    'version',
 ]


# Constants.
PYINSIM_VERSION = '2.1.0'
INSIM_VERSION = 6
_TCP_BUFFER_SIZE = 2048
_UDP_BUFFER_SIZE = 512
_TIMEOUT = 0.05
_OUTGAUGE_SIZE = (92, 96)
_OUTSIM_SIZE = (64, 68)
_PACKET_MAP = {
    insim_.ISP_ISI: insim_.IS_ISI,
    insim_.ISP_VER: insim_.IS_VER,
    insim_.ISP_TINY: insim_.IS_TINY,
    insim_.ISP_SMALL: insim_.IS_SMALL,
    insim_.ISP_STA: insim_.IS_STA,
    insim_.ISP_SCH: insim_.IS_SCH,
    insim_.ISP_SFP: insim_.IS_SFP,
    insim_.ISP_SCC: insim_.IS_SCC,
    insim_.ISP_CPP: insim_.IS_CPP,
    insim_.ISP_ISM: insim_.IS_ISM,
    insim_.ISP_MSO: insim_.IS_MSO,
    insim_.ISP_III: insim_.IS_III,
    insim_.ISP_MST: insim_.IS_MST,
    insim_.ISP_MTC: insim_.IS_MTC,
    insim_.ISP_MOD: insim_.IS_MOD,
    insim_.ISP_VTN: insim_.IS_VTN,
    insim_.ISP_RST: insim_.IS_RST,
    insim_.ISP_NCN: insim_.IS_NCN,
    insim_.ISP_CNL: insim_.IS_CNL,
    insim_.ISP_CPR: insim_.IS_CPR,
    insim_.ISP_NPL: insim_.IS_NPL,
    insim_.ISP_PLP: insim_.IS_PLP,
    insim_.ISP_PLL: insim_.IS_PLL,
    insim_.ISP_LAP: insim_.IS_LAP,
    insim_.ISP_SPX: insim_.IS_SPX,
    insim_.ISP_PIT: insim_.IS_PIT,
    insim_.ISP_PSF: insim_.IS_PSF,
    insim_.ISP_PLA: insim_.IS_PLA,
    insim_.ISP_CCH: insim_.IS_CCH,
    insim_.ISP_PEN: insim_.IS_PEN,
    insim_.ISP_TOC: insim_.IS_TOC,
    insim_.ISP_FLG: insim_.IS_FLG,
    insim_.ISP_PFL: insim_.IS_PFL,
    insim_.ISP_FIN: insim_.IS_FIN,
    insim_.ISP_RES: insim_.IS_RES,
    insim_.ISP_REO: insim_.IS_REO,
    insim_.ISP_NLP: insim_.IS_NLP,
    insim_.ISP_MCI: insim_.IS_MCI,
    insim_.ISP_MSX: insim_.IS_MSX,
    insim_.ISP_MSL: insim_.IS_MSL,
    insim_.ISP_CRS: insim_.IS_CRS,
    insim_.ISP_BFN: insim_.IS_BFN,
    insim_.ISP_AXI: insim_.IS_AXI,
    insim_.ISP_AXO: insim_.IS_AXO,
    insim_.ISP_BTN: insim_.IS_BTN,
    insim_.ISP_BTC: insim_.IS_BTC,
    insim_.ISP_BTT: insim_.IS_BTT,
    insim_.ISP_RIP: insim_.IS_RIP,
    insim_.ISP_SSH: insim_.IS_SSH,
    insim_.IRP_HLR: insim_.IR_HLR,
    insim_.IRP_HOS: insim_.IR_HOS,
    insim_.IRP_SEL: insim_.IR_SEL,
    insim_.IRP_ERR: insim_.IR_ERR,
    insim_.IRP_ARQ: insim_.IR_ARQ,
    insim_.IRP_ARP: insim_.IR_ARP,
    insim_.ISP_CON: insim_.IS_CON,
    insim_.ISP_ACR: insim_.IS_ACR,
    insim_.ISP_PLC: insim_.IS_PLC,
    insim_.ISP_HLV: insim_.IS_HLV,
    insim_.ISP_OBH: insim_.IS_OBH,
    insim_.ISP_AXM: insim_.IS_AXM,
    insim_.ISP_HCP: insim_.IS_HCP,
    insim_.ISP_NCI: insim_.IS_NCI,
    insim_.ISP_JRR: insim_.IS_JRR,
    insim_.ISP_UCO: insim_.IS_UCO,
    insim_.ISP_OCO: insim_.IS_OCO,
    insim_.ISP_TTC: insim_.IS_TTC,
    insim_.ISP_SLC: insim_.IS_SLC,
    insim_.ISP_CSC: insim_.IS_CSC,
    insim_.ISP_CIM: insim_.IS_CIM,
}


# Event constants.
EVT_INIT = 256
EVT_CLOSE = 257
EVT_ERROR = 258
EVT_ALL = 259
EVT_OUTGAUGE = 260
EVT_OUTSIM = 261
EVT_TIMEOUT = 262


class InSimError(Exception):
    """InSim error."""
    pass


def insim(host='127.0.0.1', port=29999, ReqI=0, UDPPort=0, Flags=0, 
          Prefix=b'\x00', Interval=0, Admin=b'', IName=b'pyinsim', 
          name=b'localhost'):
    """Initialize a new InSim connection.
    
    Args:
        host - Host IP to connect to.
        port - Port to connect through.
        ReqI - Initialization request ID.
        UDPPort - UDP port to use for MCI and NLP packets.
        Flags - InSim initialization flags.
        Prefix - Host command prefix.
        Interval - Interval between MCI and NLP updates.
        Admin - LFS game admin password.
        IName - Short name for your program.
        name - An optional name for the connection.        
    
    Returns:
        An initialized InSim object.
    
    """
    insim = _InSim(name)
    insim._connect(host, port, UDPPort)
    insim.send(insim_.ISP_ISI,
               ReqI=ReqI,
               UDPPort=UDPPort, 
               Flags=Flags, 
               Prefix=Prefix, 
               Interval=Interval, 
               Admin=Admin, 
               IName=IName)
    return insim

    
def relay(host='isrelay.lfs.net', port=47474, ReqI=0, HName=b'', Admin=b'', 
          Spec=b'', name=b'localhost'):
    """Initialize a new InSim relay connection.
    
    Args:
        host - The InSim relay host.
        port - The InSim relay port.
        ReqI - Initialization request ID.
        HName - The name of the host to select.
        Admin - The host admin password.
        Spec - The host spectator password.
        name - An optional name for the relay connection.
    
    Returns:
        An initialized relay host.
    
    """
    relay = _InSim(name)
    relay._connect(host, port)
    if HName:
        relay.send(insim_.IRP_SEL, ReqI=ReqI, HName=HName, Admin=Admin, Spec=Spec)
    return relay
    

def outgauge(host='127.0.0.1', port=30000, callback=None, timeout=30.0, name=b'localhost'):
    """Initialize a new OutGauge connection.
    
    Args:
        host - The host to connect to.
        port - The port to connect to the host through.
        callback - An optional function to call when an OutGauge packet is received.
        timeout - Number of seconds to wait for a packet before timing out.
        name - An optional name for the connection.    
    
    Returns:
        An initialized OutGauge host.
    
    """
    outgauge = _OutSim(name, timeout)
    outgauge._connect(host, port)
    if callback:
        outgauge.bind(EVT_OUTGAUGE, callback)
    return outgauge


def outsim(host='127.0.0.1', port=30000, callback=None, timeout=30.0, name=b'localhost'):
    """Initialize a new OutSim connection.
    
    Args:
        host - The host to connect to.
        port - The port to connect to the host through.
        callback - An optional function to call when an OutSim packet is received.
        timeout - Number of seconds to wait for a packet before timing out.
        name - An optional name for the connection.    
    
    Returns:
        An initialized OutSim host.
    
    """    
    outsim_ = _OutSim(name, timeout)
    outsim_._connect(host, port)
    if callback:
        outsim_.bind(EVT_OUTSIM, callback)
    return outsim_

    
def packet(type_, **kwargs):
    """Create a packet object.
    
    Args:
        type - The type of packet to create.
        kwargs - Arguments to initialize the packet with.
        
    Returns:
        The packet object.
    
    """
    cls = _PACKET_MAP.get(type_)
    if cls:
        return cls(**kwargs)
    return None
    

def version(ver_str, or_better=True):
    """Determine if the correct version of pyinsim is installed.
    
    Args:
        ver_str - The version to check for (E.G. '2.0.0')
        or_better - Set false for the exact version to be checked.
        
    Returns:
        True if the correct version of pyinsim is installed.
    
    """
    if or_better:
        return PYINSIM_VERSION >= ver_str
    return PYINSIM_VERSION == ver_str


def run(background=False):
    """Begin the packet receive loop.
    
    Args:
        background - Set true to run the loop in a background thread (for use in GUI app).
    
    """
    if background:
        threading.Thread(target=asyncore.loop, args=[_TIMEOUT]).start()
    else:
        asyncore.loop(timeout=_TIMEOUT)


def isrunning():
    """Determin if pyinsim is running."""
    return bool(asyncore.socket_map)


def closeall():
    """Close all open connections."""
    asyncore.close_all(ignore_all=True)


class _TcpSocket(asyncore.dispatcher):
    """Class to handle a TCP socket."""
    def __init__(self, dispatch_to):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self._dispatch_to = dispatch_to
        self._send_buff = b''
        self._recv_buff = b''
        
    def __len__(self):
        return len(self._recv_buff)
        
    def handle_connect(self):
        self._dispatch_to._handle_connect()
    
    def handle_close(self):
        self._dispatch_to._handle_close()
        
    def send(self, data):
        self._send_buff += data
        
    def writable(self):
        return bool(self._send_buff)
    
    def handle_write(self):
        sent = asyncore.dispatcher.send(self, self._send_buff)
        self._send_buff = self._send_buff[sent:]
        
    def handle_read(self):
        data = self.recv(_TCP_BUFFER_SIZE)
        if data:
            self._recv_buff += data
            self._dispatch_to._handle_tcp_read()
            
    def handle_error(self):
        self._dispatch_to._handle_error()
        
    def get_packets(self):
        while self._recv_buff and len(self._recv_buff) >= self._recv_buff[0]:
            size = self._recv_buff[0]
            
            # Check size is multiple of four.
            if size % 4 > 0:
                raise InSimError('TCP packet size not a multiple of four')
                    
            yield self._recv_buff[:size]
            self._recv_buff = self._recv_buff[size:]
        

class _UdpSocket(asyncore.dispatcher):
    """Class to handle a UDP socket."""
    def __init__(self, dispatch_to, timeout):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._dispatch_to = dispatch_to
        self._recv_buff = b''        
        self._timeout = timeout
        self.connected = False
        
    def writable(self):
        return False
        
    def readable(self):
        if self.connected:
            if self._timeout and time.time() > self._next_packet:
                self._dispatch_to._handle_timeout()
                return False
        else:
            self._next_packet = time.time() + self._timeout
            self.connected = True
        return True
        
    def handle_read(self):
        self._recv_buff = self.recv(_UDP_BUFFER_SIZE)
        if self._recv_buff:
            # Check received packet is multiple of four.
            if len(self._recv_buff) % 4 > 0:
                raise InSimError('UDP packet not a multiple of four')
            
            self._dispatch_to._handle_udp_read()
            if self._timeout:
                self._next_packet = time.time() + self._timeout
            
    def handle_error(self):
        self._dispatch_to._handle_error()
        
    def handle_close(self):
        self._dispatch_to._handle_close()
        
    def has_packet(self):
        return bool(self._recv_buff)
    
    def get_packet(self):
        return self._recv_buff     
        
        
class _Binding(object):
    """Class to manage event bindings."""
    def __init__(self):
        """Create a new _Binding object."""
        self._callbacks = {}
        
    def bind(self, evt, callback):
        """Bind an event callback.
        
        Args:
            evt - The type of event.
            callback - The function to call when the event occurs.
        
        """
        if evt in self._callbacks:
            self._callbacks[evt].append(callback)
        else:
            self._callbacks[evt] = [callback]
        
    def unbind(self, evt, callback):
        """Unbind an event callback.
        
        Args:
            evt - The type of event.
            callback - The function to unbind.
        
        """
        if evt in self._callbacks and callback in self._callbacks[evt]:
            self._callbacks[evt].remove(callback)
            if not self._callbacks[evt]:
                del self._callbacks[evt]
                
    def isbound(self, evt, callback):
        """Determin if an event callback has been bound.
        
        Args:
            evt - The type of event.
            callback - The function to check for.
            
        Returns:
            True if the callback has been bound.
        
        """
        return evt in self._callbacks and callback in self._callbacks[evt]
    
    def dispatch(self, evt, *args):
        """Dispatch an event.
        
        Args:
            evt - The type of event.
            args - The event arguments.
        
        """
        callbacks = self._callbacks.get(evt)
        if callbacks:
            [c(self, *args) for c in callbacks]  
            
        
class _InSim(_Binding):
    """Class to manage an InSim connection with LFS."""
    def __init__(self, name=b'localhost'):
        """Create a new InSim object.
        
        Args:
            name - An optional name for the connection.
        
        """
        _Binding.__init__(self)
        self.name = name
        self.hostaddr = ()
        self.connected = False
        self._tcp = _TcpSocket(dispatch_to=self)
        self._udp = _UdpSocket(dispatch_to=self, timeout=0)
            
    def _connect(self, host, port, udpport=0):
        self.hostaddr = (host, port)
        self._tcp.connect((host, port))
        if udpport:
            self._udp.bind((host, udpport))           
            
    def close(self):
        """Close the InSim connection."""
        self.connected = False
        self._tcp.close()
        self._udp.close()
        
    def send(self, type_, **kwargs):
        """Send a packet to InSim.
        
        Args:
            type - Type of packet to send.
            kwargs - The keyword arguments to initialize the packet with
        
        Returns:
            The packet that was sent.
        
        """
        packet = _PACKET_MAP[type_](**kwargs)
        self._tcp.send(packet.pack())
        return packet
        
    def sendp(self, *packets):
        """Send packets to InSim.
        
        Args:
            packets - A sequence of packets to send.
        
        """
        [self._tcp.send(packet.pack()) for packet in packets]
        
    def sendm(self, msg, ucid=0, plid=0):
        """Send a message or command to InSim.
        
        Args:
            msg - The message to send.
            ucid - The ID of the connection to send the message to.
            plid - The ID of the player to send the message to.
        
        """
        if ucid or plid:
            self._tcp.send(insim_.IS_MTC(Msg=msg, UCID=ucid, PLID=plid).pack())
        elif msg.startswith(b'/') and len(msg) < 64:
            self._tcp.send(insim_.IS_MST(Msg=msg).pack())            
        elif len(msg) < 96:
            self._tcp.send(insim_.IS_MSX(Msg=msg).pack())
        else:
            self._tcp.send(insim_.IS_MSX(Msg=msg[:95]).pack())
            
    def _handle_connect(self):     
        self.connected = True
        self.dispatch(EVT_INIT)
        
    def _handle_close(self):
        self.close()
        self.dispatch(EVT_CLOSE)
        
    def _handle_error(self):
        self.close()
        self.dispatch(EVT_ERROR)
        traceback.print_exc()
    
    def _handle_tcp_read(self):
        for data in self._tcp.get_packets():  
            self._handle_insim_packet(data)
    
    def _handle_udp_read(self):
        data = self._udp.get_packet()
        size = len(data)
        if size in _OUTSIM_SIZE:
            callbacks = self._callbacks.get(EVT_OUTSIM)
            if callbacks:
                packet = insim_.OutSimPack().unpack(data)
                [c(self, packet) for c in callbacks]
        elif size in _OUTGAUGE_SIZE:
            callbacks = self._callbacks.get(EVT_OUTGAUGE)
            if callbacks:
                packet = insim_.OutGaugePack().unpack(data)
                [c(self, packet) for c in callbacks]
        else:
            self._handle_insim_packet(data)
    
    def _handle_insim_packet(self, data):
        ptype = data[1]
        
        # Keep alive.
        if ptype == insim_.ISP_TINY and data[3] == insim_.TINY_NONE:
            self._tcp.send(data)
            
        # Handle packet event.
        bound = self._callbacks.get(ptype)
        all_ = self._callbacks.get(EVT_ALL)
        if bound or all_:
            packet = _PACKET_MAP[ptype]().unpack(data)
            if bound:
                [c(self, packet) for c in bound]
            if all_:
                [c(self, packet) for c in all_]            
            
            
class _OutSim(_Binding):
    """Class to manage an OutGauge or OutSim connection."""
    def __init__(self, name=b'localhost', timeout=0.0):
        """Create a new OutGauge or OutSim object.
        
        Args:
            name - An optional name for the connection.
        
        """
        _Binding.__init__(self)
        self.name = name
        self.hostaddr = ()
        self._udp = _UdpSocket(dispatch_to=self, timeout=timeout)
        
    def _connect(self, host, port):
        self.hostaddr = (host, port)
        self._udp.bind((host, port))
        
    def close(self):
        """Close the connection."""
        self._udp.close()
        
    def _handle_udp_read(self):
        data = self._udp.get_packet()
        size = len(data)
        if size in _OUTSIM_SIZE:
            callbacks = self._callbacks.get(EVT_OUTSIM)
            if callbacks:
                packet = insim_.OutSimPack().unpack(data)
                [c(self, packet) for c in callbacks]
        elif size in _OUTGAUGE_SIZE:
            callbacks = self._callbacks.get(EVT_OUTGAUGE)
            if callbacks:
                packet = insim_.OutGaugePack().unpack(data)
                [c(self, packet) for c in callbacks]
    
    def _handle_close(self):
        self.close()   
        self.dispatch(EVT_CLOSE)		
    
    def _handle_error(self):
        self.close()
        self.dispatch(EVT_ERROR)
        traceback.print_exc()         
        
    def _handle_timeout(self):
        self.close()
        self.dispatch(EVT_TIMEOUT) 
    
    
if __name__ == '__main__':
    pass
    #print [d for d in dir() if not d.startswith('_') and d not in ('asyncore', 'insim_', 'socket', 'traceback', 'threading')]
    
            