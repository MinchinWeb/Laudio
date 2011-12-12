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
import mutagen
import datetime 

# Django imports
from django.conf import settings

# Laudio imports
from laudio.src.inc.debugger import LaudioDebugger
from laudio.src.inc.config import LaudioConfig
from laudio.src.inc.scan_progress import ScanProgressor
from laudio.src.song.codecs.vorbis import VorbisSong
from laudio.src.song.codecs.mp3 import Mp3Song


class MusicScanner(object):
    """
    Class for scanning the files in your collection
    
    Usage:

    scanner = MusicScanner(path) # path is optional
    scanner.scan()
    """

    def __init__(self, musicDir=LaudioConfig(settings.LAUDIO_CFG).collectionPath):
        """ Instances some attributes and sets the music directory
        
        Keyword arguments:
        musicDir -- the directory where musiccollection lies; the string
                    has to end with a slash because we save the relative
                    path
                    if not given, the collectionpath from the settings is used
        """
        self.musicDir = musicDir.encode("utf-8")
        self.scanned = 0
        self.added = 0
        self.modified = 0
        self.broken = []
        self.noRights = []
        self._debugger = LaudioDebugger()
        self.scanLog = ScanProgressor()


    def scan(self):
        """ Scans a directory recursively for ogg files """
        # scan all files
        fileList = []
        for root, directories, files in os.walk(self.musicDir):
            for name in files:
                if name.lower().endswith(".ogg") or name.lower().endswith(".oga") \
                                                 or name.lower().endswith("mp3"):
                    fileList.append( os.path.join( root, name ) )

        # add a new scan entry
        num_files = len(fileList)
        self.scanLog.setTotal(num_files)
        self._debugger.log("Music Scanner", "Begin scan of %i songs" % num_files)
        
        # now add the files to the db
        for name in fileList:
            
            # ogg vorbis
            if name.lower().endswith(".ogg") or name.lower().endswith(".oga"):
                try:
                    self._addSong( VorbisSong(name) )
                except mutagen.oggvorbis.OggVorbisHeaderError:
                    self.broken.append(name)
            # mp3
            if name.lower().endswith(".mp3"):
                self._addSong( Mp3Song(name) )
        
        self._debugger.log("Music Scanner", "Finished scan")
        
        # reset count after finish
        self.scanLog.reset()
        

    def _addSong(self, musicFile):
        """ Add a song to the database.

        Keyword arguments:
        musicFile -- The song object

        """
        self.scanLog.updateScannedTracks()
        try:
            musicFile.save()
            self.modified = musicFile.modified
            self.added = musicFile.added
        except IOError:
            self.noRights.append(musicFile.path)


    def rmNonExist(self):
        """Removes tracks from the database which are
        not on the drive any more"""
        self._debugger.log("Music Scanner", "Removing non existent songs from database")
        songs = Song.objects.all()
        for song in songs:
            if not os.path.exists(song.path):
                song.delete()
                self._debugger.log("Music Scanner", "Removed %s from db: file does \
                                    not exist any more" % song.path)


    def reset(self):
        """Removes all scanned entries from the db
        """
        # TODO: delete via raw sql
        self._debugger.log("Music Scanner", "Resetting Database")
        # Song.objects.all().delete() causes database errors
        for item in Song.objects.all():
            item.delete()
        for item in Artist.objects.all():
            item.delete()
        for item in Genre.objects.all():
            item.delete()
        for item in Album.objects.all():
            item.delete()
        for item in Playlist.objects.all():
            item.delete()
