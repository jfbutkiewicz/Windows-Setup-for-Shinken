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


class TestObjectsAndNotifWays(ShinkenTest):
    #Uncomment this is you want to use a specific configuration
    #for your test
    def setUp(self):
        self.setup_with_file('etc/nagios_objects_and_notifways.cfg')

    
    # We got strange "objects" for some contacts property when we are using notif ways
    # and asking for  broks. Search why
    def test_dummy(self):
        c_normal = self.sched.contacts.find_by_name("test_contact")
        self.assert_(c_normal is not None)
        c_nw = self.sched.contacts.find_by_name("test_contact_nw")
        self.assert_(c_nw is not None)

        b = c_normal.get_initial_status_brok()
        print "B normal", b
        self.assert_(b.data['host_notification_options'] ==  u'd,u,r,f,s')
        b2 = c_nw.get_initial_status_brok()
        print "B nw", b2
        self.assert_(b2.data['host_notification_options'] == u'')

if __name__ == '__main__':
    unittest.main()

