#!/usr/bin/env python

# Copyright (C) 2009-2011 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
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

import os
import time
import copy
import shlex
import sys
import subprocess
# We will try to read in a non blocking mode
# work only on Unix systems from now
try:
    import fcntl
except ImportError:
    fcntl = None


from shinken.util import safe_print
from shinken.log import logger

__all__ = ( 'Action' )

valid_exit_status = (0, 1, 2, 3)

only_copy_prop = ('id', 'status', 'command', 't_to_go', 'timeout', 'env', 'module_type', 'execution_time')

shellchars = ( '!', '$', '^', '&', '*', '(', ')', '~', '[', ']',
                   '|', '{', '}', ';', '<', '>', '?', '`')


# Trry to read a fd in a non blocking mode
def no_block_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ''



""" This abstract class is used just for having a common id between actions and checks """
class __Action(object):
    id = 0

    # Mix the env and the environnment variables
    # into a new local env dict
    # rmq : we cannot just update os.environ because
    # it will be also modified for all others checks
    def get_local_environnement(self):
        local_env = copy.copy(os.environ)
        for p in self.env:
            local_env[p] = self.env[p].encode('utf8')
        return local_env

        # Start this action command ; the command will be executed in a subprocess
    def execute(self):
        self.status = 'launched'
        self.check_time = time.time()
        self.wait_time = 0.0001
        self.last_poll = self.check_time
        # Get a local env variables with our additionnal values
        self.local_env = self.get_local_environnement()

        # Initialize stdout and stderr. we will read them in small parts
        # if the fcntl is available
        self.stdoutdata = ''
        self.stderrdata = ''

        return self.execute__()  ## OS specific part


    def get_outputs(self, out, max_plugins_output_length):
        #print "Get only," , max_plugins_output_length, "bytes"
        # Squize all output after max_plugins_output_length
        out = out[:max_plugins_output_length]
        # Then cuts by lines
        elts = out.split('\n')
        # For perf data
        elts_line1 = elts[0].split('|')
        # First line before | is output, and strip it
        self.output = elts_line1[0].strip()
        # Init perfdata as void
        self.perf_data = ''
        # After | is perfdata, and strip it
        if len(elts_line1) > 1:
            self.perf_data = elts_line1[1].strip()
        # Now manage others lines. Before the | it's long_output
        # And after it's all perf_data, \n join
        long_output = []
        in_perfdata = False
        for line in elts[1:]:
            # if already in perfdata, direct append
            if in_perfdata:
                self.perf_data += ' ' + line.strip()
            else: # not already in? search for the | part :)
                elts = line.split('|', 1)
                # The first part will always be long_output
                long_output.append(elts[0].strip())
                if len(elts) > 1:
                    in_perfdata = True
                    self.perf_data += ' ' + elts[1].strip()
        # long_output is all non output and perfline, join with \n
        self.long_output = '\n'.join(long_output)



    def check_finished(self, max_plugins_output_length):
        # We must wait, but checks are variable in time
        # so we do not wait the same for an little check
        # than a long ping. So we do like TCP : slow start with *2
        # but do not wait more than 0.1s.
        self.last_poll = time.time()

        if self.process.poll() is None:
            self.wait_time = min(self.wait_time*2, 0.1)
            #time.sleep(wait_time)
            now = time.time()

            # If the fcntl is available (unix) we try to read in a
            # asyncronous mode, so we won't block the PIPE at 64K buffer
            # (deadlock...)
            if fcntl:
                self.stdoutdata += no_block_read(self.process.stdout)
                self.stderrdata += no_block_read(self.process.stderr)

            
            if (now - self.check_time) > self.timeout:
                self.kill__()
                #print "Kill for timeout", self.process.pid, self.command, now - self.check_time
                self.status = 'timeout'
                self.execution_time = now - self.check_time
                self.exit_status = 3
                return
            return

        # Get standards outputs from the communicate function if we do not
        # have the fcntl module (Windows, and maybe some special unix like AIX)
        if not fcntl:
            (self.stdoutdata, self.stderrdata) = self.process.communicate()
        else: # maybe the command was too quick and finish before we an poll it
              # so we finish the read
            self.stdoutdata += no_block_read(self.process.stdout)
            self.stderrdata += no_block_read(self.process.stderr)

        self.exit_status = self.process.returncode

        # we should not keep the process now
        del self.process

        # if the exit status is anormal, we add stderr to the output
        # TODO : Anormal should be logged properly no?
        if self.exit_status not in valid_exit_status:
            self.stdoutdata = self.stdoutdata + self.stderrdata
        elif 'sh: -c: line 0: unexpected EOF while looking for matching' in self.stderrdata or 'sh: Syntax error: Unterminated quoted string' in self.stderrdata:
            # Very, very ugly. But subprocess._handle_exitstatus does not see
            # a difference between a regular "exit 1" and a bailing out shell.
            # Strange, because strace clearly shows a difference. (exit_group(1) vs. exit_group(257))
            self.stdoutdata = self.stdoutdata + self.stderrdata
            self.exit_status = 3
        # Now grep what we want in the output
        self.get_outputs(self.stdoutdata, max_plugins_output_length)

        # We can clean the useless properties now
        del self.stdoutdata
        del self.stderrdata

        self.status = 'done'
        self.execution_time = time.time() - self.check_time


    def copy_shell__(self, new_i):
        # This will assign the attributes present in 'only_copy_prop' from self to new_i
        for prop in only_copy_prop:
            setattr(new_i, prop, getattr(self, prop))
        return new_i


    def got_shell_characters(self):
        for c in self.command:
            if c in shellchars:
                return True
        return False


###
## OS specific "execute__" & "kill__" are defined by "Action" class definition:

if os.name != 'nt': 
    
    class Action(__Action):
  
        # We allow direct launch only for 2.7 and higher version
        # because if a direct launch crash, under this the file handles
        # are not releases, it's not good.
        def execute__(self, force_shell=sys.version_info < (2, 7)):
            # If the command line got shell characters, we should go in a shell
            # mode. So look at theses parameters
            force_shell |= self.got_shell_characters()
            
            # 2.7 and higer Python version need a list of args for cmd
            # and if not force shell (if, it's useless, even dangerous)
            # 2.4->2.6 accept just the string command
            if sys.version_info < (2, 7) or force_shell:
                cmd = self.command.encode('utf8', 'ignore')    
            else:
                try:
                    cmd = shlex.split(self.command.encode('utf8', 'ignore'))
                except Exception, exp:
                    self.output = 'Not a valid shell command: ' + exp.__str__()
                    self.exit_status = 3
                    self.status = 'done'
                    self.execution_time = time.time() - self.check_time
                    return


#            safe_print("Launching", cmd)
#            safe_print("With env", self.local_env)

            # Now : GO for launch!
            # The preexec_fn=os.setsid is set to give sons a same process group
            # CF http://www.doughellmann.com/PyMOTW/subprocess/ for detail about this
            try:
                self.process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    close_fds=True, shell=force_shell, env=self.local_env,
                    preexec_fn=os.setsid)
            except OSError , exp:
                logger.log("Debug : Error in launching command: %s %s %s" % (self.command, exp, force_shell))
                # Maybe it's just a shell we try to exec. So we must retry
                if not force_shell and exp.errno == 8 and exp.strerror == 'Exec format error':
                    return self.execute__(True)
                self.output = exp.__str__()
                self.exit_status = 2
                self.status = 'done'
                self.execution_time = time.time() - self.check_time
  
                # Maybe we run out of file descriptor. It's not good at all!
                if exp.errno == 24 and exp.strerror == 'Too many open files':
                    return 'toomanyopenfiles'


        def kill__(self):
            # We kill a process group because we launched them with preexec_fn=os.setsid and
            # so we can launch a whole kill tree instead of just the first one
            os.killpg(self.process.pid, 9)
  
else:

    import ctypes
    TerminateProcess = ctypes.windll.kernel32.TerminateProcess

    class Action(__Action):
        def execute__(self):
            # 2.7 and higer Python version need a list of args for cmd
            # 2.4->2.6 accept just the string command
            if sys.version_info < (2, 7):
                cmd = self.command
            else:
                try:
                    cmd = shlex.split(self.command.encode('utf8', 'ignore'))
                except Exception, exp:
                    self.output = 'Not a valid shell command: ' + exp.__str__()
                    self.exit_status = 3
                    self.status = 'done'
                    self.execution_time = time.time() - self.check_time
                    return

            try:
                self.process = subprocess.Popen(cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.local_env, shell=True)
            except WindowsError, exp:
                logger.log("We kill the process : %s %s" % (exp, self.command))
                self.status = 'timeout'
                self.execution_time = time.time() - self.check_time
  
        def kill__(self):
            TerminateProcess(int(self.process._handle), -1)      

