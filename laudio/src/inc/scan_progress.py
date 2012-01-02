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
along with Laudio.  If not, see <http://www.gnu.org/licenses/>.

"""


# Django imports
from django.conf import settings

class ScanProgressor(object):
    """
    This class is responsible for reading and writing progress information
    which can be accessed by the webinterface for showing a progressbar
    or denying a scan when one is already in progress
    """

    def __init__(self):
        """
        Constructor
        """
        self.log = settings.SCAN_LOG 
        self.scanned = 0


    def setTotal(self, total=0):
        """
        Sets the total count

        Keyword arguments:

        total -- The total number of tracks
        """
        self.total = total


    def updateScannedTracks(self, by=1, offset=10):
        """
        Increments the number of scanned tracks by a certain number
        and writes them to a file determined by the given offset
        """
        self.scanned += by
        if self.scanned % offset == 0:
            self._flush()


    def isScanning(self):
        """
        Returns true if scanning is active
        """
        
        # TODO: is this really a good way to check if scanning is done?
        # For instance when the program is killed the file with tracks
        # and its content will still remain and prevent future scan
        # This should be implement with checking for a running process
        # rather than a file
        return False
        #scanned, total = self.getScannedTracks()
        #if scanned == 0 and total == 0:
        #    return False
        #else:
        #    return True


    def _flush(self, reset=False):
        """
        Writes the current values into the log file
        
        Keyword arguments:
        
        reset -- If True, sets both values to 0 in the logfile
        """
        with open(settings.SCAN_LOG, 'w') as l:
            if reset:
                self.scanned = 0
                self.total = 0
            l.write( '%s %s' % (self.scanned, self.total) )


    def reset(self):
        """
        Resets the scanned tracks file by setting the values
        to 0
        """
        self._flush(True)
        

    def getScannedTracks(self):
        """
        Returns the number of scanned and total tracks
        """
        with open(self.log, 'r') as l:
            data = l.read()
        try:
            count = data.split(' ')
            scanned = count[0] 
            total = count[1]
        except IndexError:
            scanned = 0
            total = 0
        return scanned, total

