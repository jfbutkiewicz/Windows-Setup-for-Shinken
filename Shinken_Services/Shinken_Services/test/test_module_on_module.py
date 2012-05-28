#!/usr/bin/env python2.6
#Copyright (C) 2009-2010 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
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

#
# This file is used to test reading and processing of config files
#

#It's ugly I know....
from shinken_test import *


class TestModuleOnModule(ShinkenTest):
    #Uncomment this is you want to use a specific configuration
    #for your test
    def setUp(self):
        self.setup_with_file('etc/nagios_module_on_module.cfg')

    
    #Change ME :)
    def test_module_on_module(self):
        #
        # Config is not correct because of a wrong relative path
        # in the main config file
        #
        print "Get the hosts and services"
        now = time.time()
        mod1 = self.sched.conf.modules.find_by_name("Simple-log")
        self.assert_(mod1 is not None)
        print "Got module", mod1.get_name()
        mod_sub = self.sched.conf.modules.find_by_name("ToNdodb_Mysql")
        self.assert_(mod_sub is not None)
        print "Got sub module", mod_sub.get_name()
        self.assert_(mod_sub in mod1.modules)
        self.assert_(mod_sub.modules == [])


if __name__ == '__main__':
    unittest.main()

