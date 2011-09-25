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
import os
import ConfigParser

# Django imports
from django.conf import settings


class LaudioConfig(object):
"""
Interface for writing to the config file
"""
    
    def __init__(self, configFilePath=settings.LAUDIO_CFG):
        """Constructor
    
        Keyword arguments:
        configFilePath -- The path to the config file
                         relatively to the project directory
        """
        self.configFilePath = configFilePath
        # read in config
        config = ConfigParser.SafeConfigParser(allow_no_value=True)
        config.read(self.configFilePath)
        self.collectionPath = config.get("settings", "collection_path")
        self.collectionStartup = config.getboolean("settings", "collection_startup")
        self.requireLogin = config.getboolean("settings", "require_login")
        self.debug = config.getboolean("settings", "debug")
        self.hidePlaylist = config.getboolean("settings", "hide_playlist")
        self.hideSidebar = config.getboolean("settings", "hide_sidebar")

    def save(self):
        """Writes the current values into the configfile
        """
        config = ConfigParser.SafeConfigParser()
        config.read(self.configFilePath)
        config.add_section("settings")
        config.set("settings", "collection_path", self.collectionPath)
        config.set("settings", "collection_startup", self.collectionStartup)
        config.set("settings", "require_login", self.requireLogin)
        config.set("settings", "debug", self.debug)
        config.set("settings", "hide_playlist", self.hidePlaylist)
        config.set("settings", "hide_sidebar", self.hideSidebar)
        with open(self.configFilePath, 'wb') as confFile:
            config.write(confFile)


