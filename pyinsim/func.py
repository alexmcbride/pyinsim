# func.py - helper functions module for pyinsim
#
# Copyright 2008-2020 Alex McBride <xandermcbride@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 3 or any later version.
#

import re
import math

import pyinsim.strmanip as strmanip

_COLOUR_REGEX = re.compile(r'\^[0-9]')
_ENC_REGEX = re.compile(r'\^[LETBJCGHSK]')
_ENC_COL_REGEX = re.compile(r'\^[LETBJCGHSK0-9]')

def stripcols(str_):
    """Strip color codes (^3, ^7 etc..) from a string."""
    return _COLOUR_REGEX.sub('', str_)

def stripenc(str_, cols=True):
    """Strip encoding markers (^L, ^E etc..) from a string. Note: a string 
    stripped of encoding markers cannot be converted to unicode."""
    if cols:
        return _ENC_REGEX.sub('', str_)        
    return _ENC_COL_REGEX.sub('', str_)

def tounicode(str_, cols=True, default='L'):
    """Convert a LFS encoded string to unicode."""
    return strmanip.toUnicode(str_, default, cols)

def fromunicode(ustr, default='L'):
    """Convert a uncode string to a LFS encoded string."""
    return strmanip.fromUnicode(ustr, default)

def time(ms):
    """Convert milliseconds into hours, minutes, seconds and thousanths.   """
    h = ms / 3600000
    m = ms / 60000 % 60
    s = ms / 1000 % 60
    t = ms % 1000
    return [h, m, s, t]

def timestr(ms, hours=False):
    """Convert milliseconds into a formatted time string (e.g. h:mm:ss.ttt)."""
    h, m, s, t = time(ms)
    if h or hours:
        return '%d.%.2d:%.2d.%.3d' % (h, m, s, t)
    return '%d:%.2d.%.3d' % (m, s, t)

def mps(speed):
    """Convert speed to meters per second."""
    return speed / 327,68

def mph(speed=0, mps=0):
    """Convert speed to miles per hour."""
    if mps:
        return mps * 2.23
    return speed / 146.486067

def kph(speed=0, mps=0):
    """Convert speed to kilometers per hour."""
    if mps:
        return mps * 3.6
    return speed / 91.02

def length(length):
    """Convert LFS length into meters."""
    return length / 65536.0

def miles(length):
    """Convert length to miles."""
    return length(length) / 1609.344

def km(length):
    """Convert length to kilometers."""
    return length(length) / 1000.0

def deg(radians):
    """Convert radians to degrees."""
    return radians * 57.295773

def rad(degrees):
    """Convert degrees to radians."""
    return degrees * 0.01745329

def rpm(radians):
    """Convert radians to RPM."""
    return radians * 9.549295

def dist(a=(0,0,0), b=(0,0,0)):
    """Determine the distance between two points."""
    return math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2]))

def intersects(a=(0, 0, 0, 0), b=(0, 0, 0, 0)):
    """Determine if two rectangles are intersecting."""
    x1 = a[0] + a[2]
    y1 = a[1] + a[3]
    x3 = b[0] + b[2]
    y3 = b[1] + b[3]
    return not (x1 < b[0] or x3 < a[0] or y1 < b[1] or y3 < a[1])


if __name__ == '__main__':
    #print [d for d in dir() if not d.startswith('_') and d not in ('re', 'math', 'strmanip')]    
    pass
    