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

# Django imports
from django.conf import settings

# Laudio imports
from laudio.src.inc.debugger import LaudioDebugger
from laudio.player.models import Song as SongModel
from laudio.player.models import Artist as ArtistModel
from laudio.player.models import Album as AlbumModel
from laudio.player.models import Genre as GenreModel


class Song(object):
    """
    This is a baseclass for songs which provides methods to save and update
    a song in the database. This class is abstract and should not be instantiated
    by itself
    
    Usage:
    
    # we have to use an inherited class, for instance CodecClass    
    song = CodecClass("/path/to/file.codec")
    song.save()
    
    """
    
    # static vars for debug purposes
    added = 0
    modified = 0


    def __init__(self, path):
        """Generates the javascript from templates

        Keyword arguments:
        path -- The path to the song
        """
        self.path = path
        self.modified = False
        self.added = False
        self.date = 0
        self.artist = ''
        self.title = ''
        self.album = ''
        self.genre = ''
        self.length = 0
        self.bitrate = 0
        self.tracknumber = 0
        self.size = os.path.getsize(self.path) 
        self.lastModified = datetime.datetime.fromtimestamp( os.stat(path).st_mtime )
        self._debugger = LaudioDebugger()


    def __setattr__(self, name, value):
        """Setter"""
        
        # check and correct weird dates
        if name == 'date':
            if isinstance(value, str):
                regex = r'^(\d{1,4})-?.*'
                year = re.search(regex, value)
                try:
                    if year:
                        value = int( year.group(1) )
                except ValueError:
                    value = ''
                    
        # handle empty titles
        elif name == 'title' and value == '':
            value = os.path.basename(self.path)
                
        object.__setattr__(self, name, value)
    
    
    def getModel(self):
        """
        Checks if the song exists in the database. To do this, the
        path in the database is compared to the path of the song object.
        If the two paths match, then the song model which we have to
        use is returned, otherwise false
        """
        try:
            song = SongModel.objects.get(path=self.path)
            return song
        except SongModel.DoesNotExist:
            return SongModel()
    

    def isModified(self, song):
        """
        Returns true if the timestamp from the file is newer than the 
        Database entry
        
        Keyword arguments
        song -- The database instance of a song. If song is not given
                a new song will be created and saved in the database 
        """
        return song.lastmodified != self.lastModified


    def save(self):
        """
        Saves the values of the object into the database
        """
        # get the database model of the song
        modi = True
        song = self.getModel()
        if not song.lastmodified:
            modi = False
            song.lastmodified = 0

        # only save to database if song is modified
        if self.isModified(song):
            # debug
            if modi:
                self.modfied = True
                self._debugger.log("Music Scanner", "modified %s" % self.path)
            else:
                self.added = True
                self._debugger.log("Music Scanner", "added %s" % self.path)

            # Get artist if artist is already in the database and do the same
            # for album and genre
            try:
                artist = ArtistModel.objects.get(name=self.artist)
            except ArtistModel.DoesNotExist:
                artist = ArtistModel()
                artist.name = self.artist
                artist.save()
            try:
                album = AlbumModel.objects.get(name=self.album)
            except AlbumModel.DoesNotExist:
                album = AlbumModel()
                album.name = self.album
                album.date = self.date
                album.save()
            try:
                genre = GenreModel.objects.get(name=self.genre)
            except GenreModel.DoesNotExist:
                genre = GenreModel()
                genre.name = self.genre
                genre.save()
            
            for attr in ('title', 'tracknumber', 'codec', 'bitrate', 
                         'length', 'path', 'size'):
                setattr( song, attr, getattr(self, attr) )
            
            song.lastmodified = self.lastModified
            song.artist = artist
            song.album = album
            song.genre = genre
            song.save()
