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
import hashlib
import time

# Django imports
from django.db.models import Count, Sum
from django.shortcuts import render
from django.conf import settings

# Laudio imports
from laudio.player.models import Song, Album, Genre, Artist, XMLAPIUser
from laudio.src.inc.decorators import check_token
from laudio.src.inc.config import LaudioConfig
from laudio.src.inc.shortcuts import get_var

def xml_api(request):
    """Root view for the AMPACHE XML API
    
    http://ampache.org/wiki/dev:xmlapi:development
    """
    config = LaudioConfig(settings.LAUDIO_CFG)
    
    # check if xml api is enabled
    if not config.xmlAuth:
        ctx = {
            'code': 501,
            'msg': 'XML API is not activated'
        }
        return render(request, 'xml/error.xml', ctx)
    
    # get action
    action = get_var(request, 'action')
    if action == 'handshake':
        return xml_handshake(request)
    elif action == 'ping':
        return xml_ping(request)
    elif action == 'url_to_song':
        return xml_url_to_song(request)
    elif action == 'artists':
        return xml_artists(request)
    elif action == 'artist_songs':
        return xml_artist_songs(request)
    elif action == 'album_songs':
        return xml_album_songs(request)
    elif action == 'tags':
        return xml_tags(request)
    elif action == 'tag':
        return xml_tag(request)
    elif action == 'tag_artists':
        return xml_tag_artists(request)
    elif action == 'tag_albums':
        return xml_tag_albums(request)
    elif action == 'tag_songs':
        return xml_tag_songs(request)
    elif action == 'songs':
        return xml_songs(request)
    elif action == 'song':
        return xml_song(request)
    elif action == 'playlists':
        return xml_playlists(request)
    elif action == 'playlist':
        return xml_playlist(request)
    elif action == 'playlist_songs':
        return xml_playlist_songs(request)
    elif action == 'search_songs':
        return xml_search_songs(request)
    elif action == 'videos':
        return xml_videos(request)
    elif action == 'video':
        return xml_video(request)
    # return unknown method error
    else:
        ctx = {
            'code': 405,
            'msg': 'Unknown request method'
        }
        return render(request, 'xml/error.xml', ctx)


def xml_handshake(request):
    """
    Handles the xml handshake
    """
    # get params which we need
    auth = get_var(request, 'auth')
    timestamp = get_var(request, 'timestamp')
    version = get_var(request, 'version')
    user = get_var(request, 'user')
    
    # handle auth
    try:
        xml_user = XMLAPIUser.objects.get(username=user)
    except XMLAPIUser.DoesNotExist:
        ctx = {
            'code': 400,
            'msg': 'User does not exist'
        }
        return render(request, 'xml/error.xml', ctx)
    
    # compare password phrases
    key = xml_user.password
    passphrase = hashlib.sha256( '%s%s' % (timestamp, key) )
    if passphrase != auth:
        ctx = {
            'code': 400,
            'msg': 'Password is wrong'
        }
        return render(request, 'xml/error.xml', ctx)
    
    # if login is ok, generate token and save/update it
    token = hashlib.sha256( '%i%s' % (time.time(), passphrase) )
    xml_user.last_handshake = datetime.datetime.now()
    xml_user.token = token
    xml_user.save()

    songs = Song.objects.aggregate( Count("id") )["id__count"]
    artists = Artist.objects.aggregate( Count("id") )["id__count"]
    albums = Album.objects.aggregate( Count("id") )["id__count"]
    genres = Genre.objects.aggregate( Count("id") )["id__count"]
    
    # we do not support this so set dummies
    version = 360000
    videos = 0
    catalogs = 1
    
    # get dates
    newest_song = Song.objects.all().order_by('-modified')[:1]
    if len(newest_song) != 0:
        # FIXME: are all the same? do we need this?
        add = update = clean = newest_song.isoformat()
    else:
        add = update = clean = datetime.datetime.now().isoformat()

    ctx = {
        'token': token,
        'version': version,
        'update': update,
        'add': add,
        'clean': clean,
        'song_num': songs,
        'artist_num': artists,
        'album_num': albums,
        'genre_num': genres,
        'video_num': videos,
        'catalog_num': catalogs
    }
    return render(request, 'xml/auth.xml', ctx)



######################################NOT IMPLEMENTED YET#######################
# check http://ampache.org/wiki/dev:xmlapi

@check_token
def xml_url_to_song(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)

@check_token
def xml_ping(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/ping.xml', ctx)

@check_token
def xml_artists(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/artist.xml', ctx)
    
@check_token
def xml_artist_songs(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)

@check_token
def xml_album_songs(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/songs.xml', ctx)
    
@check_token
def xml_tags(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/tag.xml', ctx)

@check_token
def xml_tag(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/tag.xml', ctx)

@check_token
def xml_tag_artists(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/artist.xml', ctx)

@check_token
def xml_tag_songs(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)
    
@check_token
def xml_tag_albums(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/album.xml', ctx)
    
@check_token
def xml_songs(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)
    
@check_token
def xml_song(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)
    
@check_token
def xml_playlists(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/playlist.xml', ctx)
    
@check_token
def xml_playlist(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/playlist.xml', ctx)

@check_token
def xml_playlist_songs(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)
    
@check_token
def xml_search_songs(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/song.xml', ctx)
    
@check_token
def xml_videos(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/video.xml', ctx)
    
@check_token
def xml_video(request):
    """Description
    """
    ctx = {}
    return render(request, 'xml/video.xml', ctx)
