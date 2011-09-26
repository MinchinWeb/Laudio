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
from laudio.src.song.formats.ogg import OGGSong
from laudio.src.song.formats.mp3 import MP3Song
from laudio.player.models import Song, Artist, Album, Genre
from laudio.inc.debugger import LaudioDebugger
from laudio.inc.config import LaudioConfig


class MusicScanner (object):
    """
    Class for scanning the files in your collection
    """

    def __init__(self, musicDir=False):
        """ Instances some attributes and sets the music directory
        
        Keyword arguments:
        musicDir -- the directory where musiccollection lies; the string
                    has to end with a slash because we save the relative
                    path
        
        """
        config = LaudioConfig()

        if musicDir:
            self.musicDir = musicDir.encode("utf-8")
        else:
            self.musicDir = config.collectionPath.encode("utf-8")       
        
        self.scanned = 0
        self.added = 0
        self.modified = 0
        self.broken = []
        self.noRights = []
        self._debugger = LaudioDebugger()
        self.debug = config.debug 


    def scan(self):
        """ Scans a directory recursively for ogg files """
        # reset count
        self._updateScanCount(True)
        # scan all files
        fileList = []
        for root, directories, files in os.walk(self.musicDir):
            for name in files:
                if name.lower().endswith(".ogg") or name.lower().endswith(".oga") \
                                                 or name.lower().endswith("mp3"):
                    fileList.append( os.path.join( root, name ) )
        # add a new scan entry
        self.total = len(fileList)
        if self.debug:
            self._debug("Begin Scan")
        # now add the files to the db
        for name in fileList:
            # TODO: check for ogg audio in the file rather then extension
            #       possible ogv files could be falsy indexed by this
            # ogg vorbis
            if name.lower().endswith(".ogg") or name.lower().endswith(".oga"):
                if self.debug:
                    self._debug("Scanned %s" % name)
                self._addSong( OGGSong(name) )
                self._updateScanCount()
            # mp3
            if name.lower().endswith(".mp3"):
                if self.debug:
                    self._debug("Scanned %s" % name)
                self._addSong( MP3Song(name) )
                self._updateScanCount()
        if self.debug:
            self._debug("Finished Scan")
        

    def _addSong(self, musicFile):
        """ Add a song to the database.

        Keyword arguments:
        musicFile -- The song object

        """
        try:
            try:
                # check if the unique path exists in the db
                song = Song.objects.get(path=musicFile.path)
                # if last modified date changed, update the songdata
                lastModified = datetime.datetime.now()
                if musicFile.lastmodified != lastModified:
                    try:
                        # Get artist 
                        try:
                            artist = Artist.objects.get(name=musicFile.artist)
                        except Artist.DoesNotExist:
                            artist = Artist(name=musicFile.artist)
                            artist.save()

                        # Get genre
                        try:
                            genre = Genre.objects.get(name=musicFile.genre)
                        except Genre.DoesNotExist:
                            genre = Genre(name=musicFile.genre)
                            genre.save()

                        # Get album
                        try:
                            album = Album.objects.get(name=musicFile.album,
                                                      artist=artist,
                                                      date=musicFile.date)
                        except Album.DoesNotExist:
                            album= Album(name=musicFile.album,
                                         artist=artist,
                                         date=musicFile.date)
                            album.save()

                        # Now set song metadata
                        for attr in ('title', 'tracknumber', 'codec', 'bitrate', 
                                     'length', 'date', 'path'):
                            setattr( song, attr, getattr(musicFile, attr) )
                        song.lastmodified = lastModified
                        song.album = album
                        song.genre = genre
                        song.save()
                        self.modified += 1
                        self._debug("modified %s in the db" % musicFile.path)
                    # broken ogg file
                    except mutagen.oggvorbis.OggVorbisHeaderError:
                        self.broken.append(musicFile.path)
            except Song.DoesNotExist:
                # if song does not exist, add a new line to the db
                try:
                    # Get artist 
                    try:
                        artist = Artist.objects.get(name=musicFile.artist)
                    except Artist.DoesNotExist:
                        artist = Artist(name=musicFile.artist)
                        artist.save()

                    # Get genre
                    try:
                        genre = Genre.objects.get(name=musicFile.genre)
                    except Genre.DoesNotExist:
                        genre = Genre(name=musicFile.genre)
                        genre.save()

                    # Get album
                    try:
                        album = Album.objects.get(name=musicFile.album,
                                                  artist=artist,
                                                  date=musicFile.date)
                    except Album.DoesNotExist:
                        album= Album(name=musicFile.album,
                                     artist=artist
                                     date=musicFile.date)
                        album.save()

                    # Now set song metadata
                    song = Song()
                    for attr in ('title', 'tracknumber', 'codec', 'bitrate', 
                                 'length', 'date', 'path'):
                        setattr( song, attr, getattr(musicFile, attr) )
                    
                    song.lastmodified = lastModified
                    song.album = album
                    song.genre = genre
                    song.save()
                    self.added += 1
                    self._debug("added %s to the db" % musicFile.path)
                # broken ogg file
                except mutagen.oggvorbis.OggVorbisHeaderError:
                    self.broken.append(musicFile.path)
        except IOError:
            self.noRights.append(musicFile.path)


    def _debug(self, msg):
        """If no debug log exists, we make a new one"""
        self._debugger.log("Music Scanner", msg)


    def _updateScanCount(self, reset=False):
        """Updates values in the scan log"""
        if reset == True:
            f = open(settings.SCAN_LOG, 'w')
            f.write( '%s %s' % (0, 1) )
            f.close()
        else:
            self.scanned += 1
            # open file only for every ten songs
            if self.scanned % 10 == 0:
                f = open(settings.SCAN_LOG, 'w')
                f.write( '%s %s' % (self.scanned, self.total) )
                f.close()


