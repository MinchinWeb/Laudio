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
from time import time
from mutagen.oggvorbis import OggVorbis

# Laudio imports
from laudio.src.song.song import Song


class VorbisSong(Song):
    """
    This class is used for handling ogg vorbis songs
    """

    def __init__(self, path):
        """ Read metainformation from an ogg file

        Keyword arguments:
        path -- the full path to the song
        """
        super(VorbisSong, self).__init__(path)
        self.codec = 'vorbis'
        song = OggVorbis(self.path)
        
        for key in ('title', 'artist', 'album', 'genre', 'date'):
            attr = song.get(key, ('',))[0]
            setattr(self, key, attr.encode('utf-8') )
        self.bitrate = int(song.info.bitrate) / 1000
        self.length = int(song.info.length)


        # check for empty track number
        try:
            self.tracknumber = int(song['tracknumber'][0])
        except (ValueError, KeyError):
            self.tracknumber = 0
