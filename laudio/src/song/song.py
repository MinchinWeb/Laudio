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

# System imports
import datetime
import os
import re

class Song(object):

    def __init__(self, path):
        self.path = path
        self.date = 0
        self.size = os.path.getsize(self.path) 
        fstat = os.stat(path)
        self.lastModified = datetime.datetime.fromtimestamp(fstat.st_mtime)


    def setDatetime(self):
        """Converts the year to a datetime object
        """
        # extract date via regex
        regex = r"^(\d{1,4})-?.*"
        year = re.search(regex, self.date)
        # too many possible insertions allow weird dates, so we just
        # try to skip those weird ones by setting nothing
        try:
            if year:
                self.date = datetime.datetime(int(year.group(1)), 1, 1)
        except ValueError:
            self.date = ''
