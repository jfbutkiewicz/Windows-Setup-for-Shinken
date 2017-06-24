Windows-Setup-for-Shinken
=========================

Licensed under GNU Affero GPL 

Shinken is a free IT monitoring solution. based on the Nagios but fully written in python, this solution is a pretty good thing to switch from nagios. All the configuration files can be taken and re-use from nagios. Please take a look on the Shinken Web Site :

http://www.shinken-monitoring.org/

This project takes the sources of the shinken product and make them easy to install and use on the Windows Platform. By default, Shinken uses srvany.exe to publish the shinken "modules". With this project, the modules are set as services by .net 2.0 applications. All the configurations are set into .config xml files, it's easier than change the registry values.

Also based on log4net, a log system takes all the standard output into a rolling files log system. But you can also change the output log with standards log4net options...

The Installer uses InstallShield 2012 - I know that it is expensive and not easy to use, but it is also powerfull and used in many enterprises... Please consider to use the allready compiled setup if you don't have Installshield, otherwise you can also install the services with the standards visual studio tools.
