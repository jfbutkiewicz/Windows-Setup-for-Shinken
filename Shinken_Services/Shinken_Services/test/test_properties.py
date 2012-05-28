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
from shinken.property import UnusedProp, BoolProp, IntegerProp, FloatProp, CharProp, StringProp

class TestConfig(ShinkenTest):
    #Uncomment this is you want to use a specific configuration
    #for your test
    def setUp(self):
        pass

    
    #Test the bool property class
    def test_bool_property(self):
        p = BoolProp(default='1', class_inherit=[('Host', 'accept_passive_checks')])
        print p.__dict__
        s = "1"
        val = p.pythonize(s)
        print s, val
        self.assert_(val == True)
        s = "0"
        val = p.pythonize(s)
        print s, val
        self.assert_(val == False)

        #Now a service one
        p = BoolProp(default='0', fill_brok=['full_status'])
        print p.__dict__
        s = "1"
        val = p.pythonize(s)
        print s, val
        self.assert_(val == True)
        self.assert_('full_status' in p.fill_brok)
        

if __name__ == '__main__':
    unittest.main()

