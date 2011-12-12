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
import os
import MySQLdb


class ResourceChecker(object):
    """
    Checking resources class, for instance read and write rights for important
    files and database conns
    """
    
    
    def __init__(self):
        """Constructor
        """
        pass
        
        
    def is_rw(self, path):
        """Checks if a file is read and writeable
    
        Keyword arguments:
        path -- The path to the file
        """
        if not os.path.exists(path):
            return False
        if not os.access(path, os.R_OK):
            False
        if not os.access(path, os.W_OK):
            False
        
        return True
            

    def db_conn(self, user, passwd, db, host='localhost', port=3306):
        """Checks if we can connect to a database
        Returns false if no connection is possible, otherwise true
    
        Keyword arguments:
        user -- The database user
        passwd -- The database password
        db -- The database
        host -- The database host, defaults to localhost
        port -- The database port, defaults to 3306
        """
        try:
            db = MySQLdb.connect(host, user, passwd, db, port)
            db.close()
            return True
        except (TypeError, MySQLdb.Error):
            return False

