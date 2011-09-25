#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Laudio - A webbased musicplayer

Copyright (C) 2010 Bernhard Posselt, bernhard.posselt@gmx.at

Laudio is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Laudio is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

"""

# System imports
import datetime

# Django imports
from django.conf import settings


class LaudioDebugger(object):
    """
    Class for debugging
    """

    def __init__(self, logFilePath=settings.DEBUG_LOG):
        """Constructor
    
        Keyword arguments:
        logFilePath -- The path to the debug logfile
        """
        self.logFilePath = logFilePath
        self.log = {}

    def log(self, part, msg):
        """Logs a msg but doesnt write it into the log
        You have to execute flush() for writing
    
        Keyword arguments:
        part -- The area where the log belongs to
        msg -- The message which should be logged
        """
        self.log[datetime.datetime.now()] = (msg, part) 

    def flush(self):
        """Flushes all logs to the debug log file
        """
        with( open(self.logFilePath, "a+") ) as log:
            for key, value in self.log.iteritems():
                log.write("%s %s: %s \n" % (key, value[0], value[1]))
