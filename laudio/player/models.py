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
import hashlib

# Django imports
from django.conf import settings 
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



class Artist(models.Model):
    name = models.CharField(_('Artist'), max_length=150)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Artist)
    name = models.CharField(_('Album'), max_length=150)
    date = models.CharField(_('Year'), max_length=100);
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(_('Genre'), max_length=150)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def __unicode__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(_('Title'), max_length=250)
    album = models.ForeignKey(Album)
    genre = models.ForeignKey(Genre)
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


class XMLAPIUser(models.Model):
    username = models.CharField(_('Username'), max_length=250)
    password = models.CharField(_('Password'), max_length=64)
    token = models.CharField(_('Token'), max_length=64)
    last_handshake = models.DateTimeField(_('Last handshake'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    def set_password(self, password):
        self.password = hashlib.sha256(password)
        self.save()


# get themes in the themes directory
THEMES = []
for theme in os.listdir( os.path.join(settings.MEDIA_ROOT, 'themes/') ):
    THEMES.append(
        (theme, theme)
        )

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
    lastFMName = models.CharField(_('last.fm username'), max_length=100, blank=True)
    lastFMPass = models.CharField(_('last.fm password'), max_length=100, blank=True)
    lastFMSubmit = models.BooleanField(_('Scrobble last.fm'), 
        help_text=_('Activate this if you want to submit your played tracks \
                    to your last.fm account'))
    libreFMName = models.CharField(_('libre.fm username'), max_length=100, blank=True)
    libreFMPass = models.CharField(_('libre.fm password'), max_length=100, blank=True)
    libreFMSubmit = models.BooleanField(_('Scrobble libre.fm'),
        help_text=_('Activate this if you want to submit your played tracks \
                    to your libre.fm account'))
    showLib = models.BooleanField(_('Show all songs on startup'), 
                help_text=_('This displays your whole collection automatically on startup. \
                            Be carefull with bigger collections as it may impact your \
                            browser\'s speed'))
    hidePlaylist = models.BooleanField(_('Hide playlist by default'), help_text=_('Automatically \
                    hides the playlist in the Collection view so you have \
                    to click playlist to view it'))
    hideSidebar = models.BooleanField(_('Hide sidebar by default'), help_text=_('Automatically \
                    hides the sidebar in the Collection view so you have \
                    to click sidebar to view it'))
    theme = models.CharField(_('l-audio theme'), max_length=100, choices=THEMES, 
        help_text=_('Choose a custom theme'))
