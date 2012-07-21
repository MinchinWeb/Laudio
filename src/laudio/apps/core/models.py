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

from django.conf import settings 
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Artist(models.Model):
    name = models.CharField(_('Artist'), max_length=150, unique=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(_('Album'), max_length=150)
    date = models.CharField(_('Year'), max_length=100);
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(_('Genre'), max_length=150, unique=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(_('Title'), max_length=250)
    album = models.ForeignKey('Album')
    genre = models.ForeignKey('Genre')
    artist = models.ForeignKey('Artist')
    codec = models.CharField(_('Codec'), max_length=10)
    tracknumber = models.IntegerField(_('Tracknumber'))
    path = models.FilePathField(_('Path'))
    lastmodified = models.DateTimeField(_('Last metadata change'))
    added =  models.DateTimeField(_('Added'), auto_now_add=True)
    length = models.IntegerField(_('Length'))
    bitrate = models.CharField(_('Bitrate'), max_length=100);
    size = models.IntegerField(_('Size'));
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.title
        
    def rel_path(self):
        """Returns the relative path of the song
        """
        return self.path.replace(settings.LAUDIO_CONFIG.collectionPath, '', 1)


class Playlist(models.Model):
    name = models.CharField(_('Playlist'), max_length=250)
    added = models.IntegerField(_('Added'))
    songs = models.ManyToManyField(Song, through='PlaylistEntry')
    user = models.ForeignKey(User)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class PlaylistEntry(models.Model):
    playlist = models.ForeignKey(Playlist)
    song = models.ForeignKey(Song)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
