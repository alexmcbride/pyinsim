"""Example 5: Play a windows sound when the shift-light comes on"""

import sys
import pyinsim

# Check this will actually work. :p
try:
    import winsound
except ImportError:
    print('Error: this example only works on Windows')
    sys.exit()

def outgauge_packet(outgauge, packet):
    # Check for shift light flag.
    if packet.ShowLights & pyinsim.DL_SHIFT:
        # Play sound.
        winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)

# Initialize OutGauge. Set timeout to 30 seconds.
outgauge = pyinsim.outgauge('127.0.0.1', 30000, outgauge_packet, 30.0)

pyinsim.run()
