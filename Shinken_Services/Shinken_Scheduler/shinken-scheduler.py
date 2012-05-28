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


#For the Shinken application, I try to respect
#The Zen of Python, by Tim Peters. It's just some
#very goods ideas that make Python programming very fun
#and efficient. If it's good for Python, it must be good for
#Shinken. :)
#
#
#
#Beautiful is better than ugly.
#Explicit is better than implicit.
#Simple is better than complex.
#Complex is better than complicated.
#Flat is better than nested.
#Sparse is better than dense.
#Readability counts.
#Special cases aren't special enough to break the rules.
#Although practicality beats purity.
#Errors should never pass silently.
#Unless explicitly silenced.
#In the face of ambiguity, refuse the temptation to guess.
#There should be one-- and preferably only one --obvious way to do it.
#Although that way may not be obvious at first unless you're Dutch.
#Now is better than never.
#Although never is often better than *right* now.
#If the implementation is hard to explain, it's a bad idea.
#If the implementation is easy to explain, it may be a good idea.
#Namespaces are one honking great idea -- let's do more of those!


#This class is the application in charge of the scheduling
#The scheduler listens to the Arbiter for the configuration sent through 
#the port given as first argument.
#The configuration sent by the arbiter specifies which checks and actions 
#the scheduler must schedule, and a list of reactionners and pollers 
#to execute them
#When the reactionner is already launched and has its own conf, it still 
#listens to arbiter (one a timeout)
#In case the arbiter has a new conf to send, the reactionner is stopped 
#and a new one is created.

import os
import sys
import optparse


# We try to raise up recusion limit on
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

from shinken.daemons.schedulerdaemon import Shinken
from shinken.bin import VERSION


parser = optparse.OptionParser(
    "%prog [options]", version="%prog " + VERSION)
parser.add_option('-c', '--config',
                  dest="config_file", metavar="CONFIG-FILE",
                  help='Config file')
parser.add_option('-d', '--daemon', action='store_true',
                  dest="is_daemon",
                  help="Run in daemon mode")
parser.add_option('-r', '--replace', action='store_true',
                  dest="do_replace",
                  help="Replace previous running scheduler")
parser.add_option('--debugfile', dest='debug_file',
                  help=("Debug file. Default: not used "
                        "(why debug a bug free program? :) )"))
opts, args = parser.parse_args()
if args:
    parser.error("Does not accept any argument.")

# Protect for windows multiprocessing that will RELAUNCH all
if __name__ == '__main__':
    daemon = Shinken(debug=opts.debug_file is not None, **opts.__dict__)
    daemon.main()
# For perf running :
#import cProfile
#cProfile.run('''daemon.main()''', '/tmp/scheduler.profile')
