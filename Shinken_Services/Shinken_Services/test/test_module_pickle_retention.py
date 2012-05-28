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

import os
import time

from shinken_test import unittest, ShinkenTest

from shinken.log import logger
from shinken.objects.module import Module
from shinken.modules import pickle_retention_file_scheduler
from shinken.modules.pickle_retention_file_scheduler import get_instance 


modconf = Module()
modconf.module_name = "PickleRetention"
modconf.module_type = pickle_retention_file_scheduler.properties['type']
modconf.modules = []
modconf.properties = pickle_retention_file_scheduler.properties.copy()


class TestConfig(ShinkenTest):
    #setUp is in shinken_test

    #Change ME :)
    def test_pickle_retention(self):
        print self.conf.modules
        now = time.time()
        #get our modules
        mod = pickle_retention_file_scheduler.Pickle_retention_scheduler(modconf, 'tmp/retention-test.dat')
        try :
            os.unlink(mod.path)
        except :
            pass

        sl = get_instance(mod)
        print "Instance", sl
        #Hack here :(
        sl.properties = {}
        sl.properties['to_queue'] = None
        sl.init()
        l = logger

        in_the_future = now + 500
        #Now we change thing
        svc = self.sched.hosts.find_by_name("test_host_0")
        # We want it to go in the future
        svc.next_chk = in_the_future

        # By default in the conf, the active checsk are active
        self.assert_(svc.active_checks_enabled == True)
        # and passive one too
        self.assert_(svc.passive_checks_enabled == True)

        #updte the hosts and service in the scheduler in the retentino-file
        sl.hook_save_retention(self.sched)
        
        self.assert_(svc.state == 'PENDING')
        print "State", svc.state
        svc.state = 'UP' #was PENDING in the save time
        
        # We try to change active state change too
        svc.active_checks_enabled = False
        svc.passive_checks_enabled = False

        # now we try to change it
        svc.next_chk = now - 3000

        r = sl.hook_load_retention(self.sched)
        self.assert_(r == True)
        
        # Now look at checks active or not
        # Should be back as normal values :)
        self.assert_(svc.active_checks_enabled == True)
        # and passive one too
        self.assert_(svc.passive_checks_enabled == True)


        print "Fuck after load, will go in", svc.next_chk - now

        # Should be ok, because we load it from retention
        self.assert_(svc.next_chk == in_the_future)
        
        #search if the host is not changed by the loading thing
        svc2 = self.sched.hosts.find_by_name("test_host_0")
        self.assert_(svc == svc2)
        
        self.assert_(svc.state == 'PENDING')

        #Ok, we can delete the retention file
        os.unlink(mod.path)

        # Lie about us in checking or not
        svc.in_checking = False
        diff = svc.next_chk - now
        print "Fuck Ok go for a enw scheduling!", diff
        #should be near 500 seconds ahead
        self.assert_(499 < diff < 501)

        # Now we reschedule it, should be our time_to_go
        svc.schedule()
        print "Fuck after a reschedule", svc.next_chk - now
        # should be the same value in the future, we want to keep it
        diff = svc.next_chk - now
        self.assert_(499 < diff < 501)

        # Now make real loops with notifications
        self.scheduler_loop(10, [[svc, 2, 'CRITICAL | bibi=99%']])
        #updte the hosts and service in the scheduler in the retentino-file
        save_notified_contacts = svc2.notified_contacts
        print "Save notif contacts", save_notified_contacts
        sl.hook_save_retention(self.sched)

        r = sl.hook_load_retention(self.sched)
        self.assert_(r == True)
        
        print "Notif?", svc2.notified_contacts
        # We should got our contacts, and still the true objects
        self.assert_(len(svc2.notified_contacts) > 0)
        for c in svc2.notified_contacts:
            self.assert_(c in save_notified_contacts)
        


if __name__ == '__main__':
    unittest.main()

