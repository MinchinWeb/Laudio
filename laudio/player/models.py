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

from django.db import models
from django import forms
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=150)


class Album(models.Model):
    artist = models.ForeignKey(Artist)
    name = models.CharField(max_length=150)
    date = models.CharField(max_length=100);


class Genre(models.Model):
    name = models.CharField(max_length=150)


class Song(models.Model):
    title = models.CharField(max_length=250)
    album = models.ForeignKey(Album)
    genre = models.ForeignKey(Genre)
    codec = models.CharField(max_length=10)
    tracknumber = models.IntegerField()
    path = models.FilePathField()
    lastmodified = models.DateTimeField()
    added =  models.DateTimeField(auto_now_add=True)
    length = models.IntegerField()
    bitrate = models.CharField(max_length=100);


class Playlist(models.Model):
    name = models.CharField(max_length=250)
    added = models.IntegerField()
    songs = models.ManyToManyField(Song, through="PlaylistEntry")
    user = models.ForeignKey(User)


class PlaylistEntry(models.Model):
    playlist = models.ForeignKey(Playlist)
    song = models.ForeignKey(Song)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    lastFMName = models.CharField("last.fm username", max_length=100, blank=True)
    lastFMPass = models.CharField("last.fm password", max_length=100, blank=True)
    lastFMSubmit = models.BooleanField("Scrobble last.fm", 
        help_text="Activate this if you want to submit your played tracks \
                    to your last.fm account")
    libreFMName = models.CharField("libre.fm username", max_length=100, blank=True)
    libreFMPass = models.CharField("libre.fm password", max_length=100, blank=True)
    libreFMSubmit = models.BooleanField("Scrobble libre.fm",
        help_text="Activate this if you want to submit your played tracks \
                    to your libre.fm account")
    showLib = models.BooleanField("Show all songs on startup", 
                help_text="This displays your whole collection automatically on startup. \
                            Be carefull with bigger collections as it may impact your \
                            browser's speed")
    hidePlaylist = models.BooleanField("Hide playlist by default", help_text="Automatically \
                    hides the playlist in the Collection view so you have \
                    to click playlist to view it")
    hideSidebar = models.BooleanField("Hide sidebar by default", help_text="Automatically \
                    hides the sidebar in the Collection view so you have \
                    to click sidebar to view it")
