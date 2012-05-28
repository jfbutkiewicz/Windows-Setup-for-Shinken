#!/usr/bin/env python
#Copyright (C) 2009-2011 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#
#This file is part of Shinken.
#
#Shinken is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Shinken is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Shinken.  If not, see <http://www.gnu.org/licenses/>.


"""
This is the class of the Arbiter. It's role is to read configuration,
cut it, and send it to other elements like schedulers, reactionners
or pollers. It is also responsible for the high avaibility feature. 
For example, should a scheduler dies, it sends the late scheduler's conf 
to another scheduler still available.
It also reads orders form users (nagios.cmd) and sends them to schedulers.
"""


import os
import sys
import optparse



# We try to raise up recursion limit on
# but we don't have resource module on windows
if os.name != 'nt':
    import resource
    # All the pickle will ask for a lot of recursion, so we must make
    # sure to set it at a high value. The maximum recursion depth depends
    # on the Python version and the process limit "stack size".
    # The factors used were acquired by testing a broad range of installations
    stacksize_soft, stacksize_hard = resource.getrlimit(3)
    if sys.version_info < (2,6):
        sys.setrecursionlimit(int(stacksize_soft * 0.65 + 1100))
    elif sys.version_info < (3,):
        sys.setrecursionlimit(int(stacksize_soft * 1.9 + 3200))
    else:
        sys.setrecursionlimit(int(stacksize_soft * 2.4 + 3200))

try:
    from shinken.bin import VERSION
    import shinken
except ImportError:
    # If importing shinken fails, try to load from current directory
    # or parent directory to support running without installation.
    # Submodules will then be loaded from there, too.
    import imp
    imp.load_module('shinken', *imp.find_module('shinken', [os.path.realpath("."), os.path.realpath(".."), os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "..")]))
    
from shinken.bin import VERSION
from shinken.pyro_wrapper import PYRO_VERSION
from shinken.daemons.arbiterdaemon import Arbiter

parser = optparse.OptionParser(
    "%prog [options] -c configfile [-c additional_config_file]",
    version="%prog : " + VERSION + "     with pyro : " + PYRO_VERSION)
parser.add_option('-c', '--config', action='append',
                  dest="config_files", metavar="CONFIG-FILE",
                  help=('Config file (your nagios.cfg). Multiple -c can be '
                        'used, it will be like if all files was just one'))
parser.add_option('-d', '--daemon', action='store_true',
                  dest="is_daemon",
                  help="Run in daemon mode")
parser.add_option('-r', '--replace', action='store_true',
                  dest="do_replace",
                  help="Replace previous running arbiter")
parser.add_option('--debugfile', dest='debug_file',
                  help=("Debug file. Default: not used "
                        "(why debug a bug free program? :) )"))
parser.add_option("-v", "--verify-config",
                  dest="verify_only", action="store_true",
                  help="Verify config file and exit")

opts, args = parser.parse_args()


if not opts.config_files:
    parser.error("Requires at least one config file (option -c/--config")
if args:
    parser.error("Does not accept any argument. Use option -c/--config")

# Protect for windows multiprocessing that will RELAUNCH all
if __name__ == '__main__':
    daemon = Arbiter(debug=opts.debug_file is not None, **opts.__dict__)
    daemon.main()
# For perf tuning :
#import cProfile
#cProfile.run('''daemon.main()''', '/tmp/arbiter.profile')
