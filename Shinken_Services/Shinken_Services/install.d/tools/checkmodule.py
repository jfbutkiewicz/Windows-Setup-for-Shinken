#!/usr/bin/env python
#Copyright (C) 2009-2012 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    David GUENAULT, dguenault@monitoring-fr.org
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

import sys
import getopt
def main(argv):                         
	try:                                
		opts, args = getopt.getopt(argv, "m:")
		ret=0
		for o, a in opts:
			if o == "-m":
				try:
					exec("import "+a)
					print "OK"
				except:
					print "KO"
					ret=2
	except:           
		ret=1
	sys.exit(ret) 

if __name__ == "__main__":
	main(sys.argv[1:])
