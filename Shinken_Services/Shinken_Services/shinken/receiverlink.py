#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2011 :
#     Gabes Jean, naparuba@gmail.com
#     Gerhard Lausser, Gerhard.Lausser@consol.de
#     Gregory Starck, g.starck@gmail.com
#     Hartmut Goebel, h.goebel@goebel-consult.de
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.


from shinken.satellitelink import SatelliteLink, SatelliteLinks
from shinken.property import BoolProp, IntegerProp, StringProp, ListProp

class ReceiverLink(SatelliteLink):
    """Please Add a Docstring to describe the class here"""
    
    id = 0
    my_type = 'receiver'
    properties = SatelliteLink.properties.copy()
    properties.update({
        'receiver_name':        StringProp (fill_brok=['full_status'], to_send=True),
        'port':               IntegerProp(default='7772', fill_brok=['full_status']),
        'manage_sub_realms':  BoolProp   (default='1', fill_brok=['full_status']),
        'manage_arbiters':    BoolProp   (default='0', fill_brok=['full_status'], to_send=True),
    })
  
    def get_name(self):
        return self.receiver_name


    def register_to_my_realm(self):
        self.realm.receivers.append(self)




class ReceiverLinks(SatelliteLinks):
    """Please Add a Docstring to describe the class here"""
    
    name_property = "receiver_name"
    inner_class = ReceiverLink
