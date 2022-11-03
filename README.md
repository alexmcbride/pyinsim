# PYINSIM

pyinsim is a InSim module for the Python programming language. It creates 
socket connection with LFS and provides many classes, functions and 
enumerations for sending and receiving data between your program and the game.

## REQUIREMENTS

~~The module requires Python 2.7 or better to run. Note: It does not currently 
support Python 3.0.~~ 

Experimental Python 3 support, tested on Python 3.10.6.

You can download Python from the following URL:
http://www.python.org/download/

Or use Anaconda : 
https://www.anaconda.com/products/distribution

## INSTALLATION

~~To install pyinsim on Windows, simply unzip the package and run the windows
installer 'pyinsim-x.x.x.win32.exe'.~~ Not online ? 

To install from the source distribution, run the command 
```python setup.py install```, in a dedicated python environment. 

If the above doesn't work (depreciation warning), try: ```python -m pip install --user -e .```


Both of these methods will install pyinsim to your 
'X:\Path\To\Python\Lib\site-packages' directory. 

Of course you always have the option of just copying the package folder into 
your program's source directory (this is also useful for when you redistribute
your program.). But for this you'll need to check the relative imports. 

## LICENSE

pyinsim is free software: you can redistribute it and/or modify it under the 
terms of the GNU Lesser General Public License as published by the Free 
Software Foundation, either version 3 of the License, or (at your option) any 
later version.

pyinsim is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR 
A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more 
details.

You should have received a copy of the GNU Lesser General Public License along 
with pyinsim. If not, see <http://www.gnu.org/licenses/>.

## AUTHOR

Written by Alex McBride
Copyright Alex McBride 2012-2019
Website: https://github.com/alexmcbride/pyinsim

## THANKS

Thanks to Constantin Kopplinger (morpha) for his work on the strmanip module.
Thanks to tmehlinger for his work on InSim Relay support.

