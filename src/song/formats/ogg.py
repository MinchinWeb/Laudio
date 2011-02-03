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
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

import os
from time import time
from mutagen.oggvorbis import OggVorbis
from laudio.src.song.song import Song

class OGGSong (Song):

    def __init__(self, path):
        """ Read metainformation from an ogg file
        The multiple KeyErrors check if tags are not Null
        Keyword arguments:
        path -- the full path to the song
        """
        self.codec = "ogg"
        self.path = unicode(path)
        self.song = OggVorbis(self.path)
        for key in ('title', 'artist', 'album', 'genre', 'date'):
            setattr(self, key, unicode( self.song.get(key, ('',))[0] ))
        self.bitrate = int(self.song.info.bitrate) / 1000
        self.length = int(self.song.info.length)
        # check for empty track number
        try:
            self.tracknumber = int(self.song['tracknumber'][0])
        except (ValueError, KeyError):
            self.tracknumber = 0
