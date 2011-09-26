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
        try:
            config = ConfigParser.SafeConfigParser(allow_no_value=True)
            config.read(self.configFilePath)
            self.collectionPath = config.get("settings", "collection_path")
            self.collectionStartup = config.getboolean("settings", "collection_startup")
            self.requireLogin = config.getboolean("settings", "require_login")
            self.debug = config.getboolean("settings", "debug")
            self.hidePlaylist = config.getboolean("settings", "hide_playlist")
            self.hideSidebar = config.getboolean("settings", "hide_sidebar")
            self.version = config.get("settings", "version")
            self.xmlAPIAuth = config.getboolean("settings", "xml_auth")
        except ConfigParser.NoSectionError:
            # write default values
            self.collectionPath = ""
            self.collectionStartup = False
            self.requireLogin = False
            self.debug = False
            self.hidePlaylist = False
            self.hideSidebar = False
            self.xmlAPIAuth = False
            self.version = settings.LAUDIO_VERSION
            self.save()

    def save(self):
        """Writes the current values into the configfile
        """
        config = ConfigParser.SafeConfigParser()
        config.add_section("settings")
        config.set("settings", "collection_path", self.collectionPath)
        config.set("settings", "collection_startup", str(self.collectionStartup))
        config.set("settings", "require_login", str(self.requireLogin))
        config.set("settings", "debug", str(self.debug))
        config.set("settings", "hide_playlist", str(self.hidePlaylist))
        config.set("settings", "hide_sidebar", str(self.hideSidebar))
        config.set("settings", "version", self.version)
        config.set("settings", "xml_auth", str(self.xmlAPIAuth))
        with open(self.configFilePath, 'wb') as confFile:
            config.write(confFile)


