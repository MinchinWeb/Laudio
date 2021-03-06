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
import time
import datetime

# Django imports
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.db.models import Q, Count, Sum
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

# Laudio imports
from laudio.player.models import Song, Artist, Genre, Album, Playlist, PlaylistEntry
import laudio.src.scrobbler as scrobbler
from laudio.src.music_scanner import MusicScanner
from laudio.src.cover_fetcher import CoverFetcher
from laudio.src.inc.decorators import check_login
from laudio.src.inc.scan_progress import ScanProgressor
from laudio.src.inc.shortcuts import send_file, download_file, get_var, post_var

@csrf_exempt
def ajax_search(request):
    """
    Searches the database for a simple request
    """
    search = post_var(request, 'search').lower()
    # filter every appropriate column
    search = '%' + search + '%'
    # yeah we have to do this because ordering by lower doesnt work across
    # tables
    songs = Song.objects.raw(
        "SELECT sng.id AS id, \
                sng.tracknumber AS tracknumber, \
                sng.title AS title \
            FROM player_song sng \
	        LEFT JOIN player_album alb \
		        ON sng.album_id = alb.id \
	        LEFT JOIN player_artist art \
		        ON sng.artist_id = art.id \
	        LEFT JOIN player_genre gr \
		        ON sng.genre_id = gr.id \
	        WHERE \
		        LOWER(art.name) LIKE %s \
		        OR \
		        LOWER(alb.name) LIKE %s \
		        OR \
		        LOWER(gr.name) LIKE %s \
		        OR \
		        LOWER(sng.title) LIKE %s \
	        ORDER BY \
		        LOWER(art.name), LOWER(alb.name), sng.tracknumber",
		[search, search, search, search]
    )

    ctx = {
        'songs': songs,
    }
    return render(request, 'ajax/search.html', ctx)


@csrf_exempt
def ajax_search_advanced(request):
    """
    Searches the database for a complex query
    """
    artist = '%' + post_var(request, 'artist').lower() + '%'
    title = '%' + post_var(request, 'title').lower() + '%'
    genre = '%' + post_var(request, 'genre').lower() + '%'
    album = '%' + post_var(request, 'album').lower() + '%'
    
    # yeah we have to do this because ordering by lower doesnt work across
    # tables
    songs = Song.objects.raw(
        "SELECT sng.id AS id, \
                sng.tracknumber AS tracknumber, \
                sng.title AS title \
            FROM player_song sng \
	        LEFT JOIN player_album alb \
		        ON sng.album_id = alb.id \
	        LEFT JOIN player_artist art \
		        ON sng.artist_id = art.id \
	        LEFT JOIN player_genre gr \
		        ON sng.genre_id = gr.id \
	        WHERE \
		        LOWER(art.name) LIKE %s \
		        AND \
		        LOWER(alb.name) LIKE %s \
		        AND \
		        LOWER(gr.name) LIKE %s \
		        AND \
		        LOWER(sng.title) LIKE %s \
	        ORDER BY \
		        LOWER(art.name), LOWER(alb.name), sng.tracknumber",
		[artist, album, genre, title]
    )

    ctx = {
        'songs': songs,
    }
    return render(request, 'ajax/search.html', ctx)


@csrf_exempt
def ajax_search_artist_letter(request):
    """
    Searches the database for artists starting with a letter
    """
    search = post_var(request, 'search').lower()
    # filter every appropriate column
    search = search + '%'
    # yeah we have to do this because ordering by lower doesnt work across
    # tables
    songs = Song.objects.raw(
        "SELECT sng.id AS id, \
                sng.tracknumber AS tracknumber, \
                sng.title AS title \
            FROM player_song sng \
	        LEFT JOIN player_album alb \
		        ON sng.album_id = alb.id \
	        LEFT JOIN player_artist art \
		        ON sng.artist_id = art.id \
	        LEFT JOIN player_genre gr \
		        ON sng.genre_id = gr.id \
	        WHERE \
		        LOWER(art.name) LIKE %s \
	        ORDER BY \
		        LOWER(art.name), LOWER(alb.name), sng.tracknumber",
		[search, ]
    )

    ctx = {
        'songs': songs,
    }
    return render(request, 'ajax/search.html', ctx)


@check_login('admin')
#@require_POST
def ajax_scan(request):
    """
    Starts a music scan
    """
    scanner = MusicScanner()
    scanner.scan()
    ctx = {
        'scanned': scanner.scanned,
        'added': scanner.added,
        'modified': scanner.modified,
        'broken': scanner.broken,
        'no_rights': scanner.noRights
    }
    return render(request, 'ajax/scan.json', ctx)

    

@check_login('admin')
def ajax_scan_progress(request):
    """
    Returns the number of scanned and total songs
    """
    prog = ScanProgressor()
    scanned, total = prog.getScannedTracks()
    ctx = {
        'scanned': scanned,
        'total': total
    }
    return render(request, 'ajax/scan_count.json', ctx)


@check_login('admin')
@require_POST
def ajax_db_reset(request):
    """
    Deletes all songs form the database
    """
    scanner = MusicScanner()
    scanner.reset()
    ctx = {
        'msg': 'Reseted the database, deleted all songs and playlists',
        'success': 1,
    }
    return render(request, 'ajax/success.json', ctx)
 

@check_login('admin')
@require_POST
def ajax_db_rmnonexist(request):
    """
    Removes all nonexistent songentries from the database
    """
    scanner = MusicScanner()
    scanner.rmNonExist()
    ctx = {
        'msg': 'Removed all nonexistent files from the database',
        'success': 1,
    }
    return render(request, 'ajax/success.json', ctx)


@check_login('user')
def ajax_db_statistics(request):
    """
    Returns database statistics
    """
    count = Song.objects.aggregate( Count("id"), Sum("length") )
    mp3s = Song.objects.filter(codec="mp3").aggregate( Count("id") )
    oggs = Song.objects.filter(codec="vorbis").aggregate( Count("id") )
    songs = count["id__count"]
    length = count["length__sum"]
    if length == None:
        length = 0
    hours = int( length / (60 * 60) )
    days = int( hours / 24 )
    weeks = int( days / 7 )
    mp3s = mp3s["id__count"]
    oggs = oggs["id__count"]
    ctx = {
        'numberOfSongs': songs,
        'numberOfMp3s': mp3s,
        'numberOfOggs': oggs,
        'numberOfHours': hours,
        'numberOfDays': days,
        'numberOfWeeks': weeks,
    }
    return render(request, 'ajax/db_stats.json', ctx)


@check_login('user')
def ajax_song_data(request):
    """
    Returns details about one song
    """
    id = int(request.GET.get('id', ''))
    song = get_object_or_404(Song, id=id)
    ctx = {
        'song': song,
    }
    return render(request, 'ajax/song_data.json', ctx)


@check_login('user')
@require_POST
def ajax_song_scrobble(request):
    """
    Returns details about one song
    """
    id = int(request.POST.get('id', ''))
    song = get_object_or_404(Song, id=id)
    msg = ""
    success = 0
    
    # if user is logged in submit stats
    if request.user.is_authenticated():
        now = int( time.mktime(datetime.datetime.now().timetuple()) )
        userprofile = request.user.get_profile()
        # check for last.fm scrobbling
        try:
            if request.user.get_profile().lastFMSubmit:
                if userprofile.lastFMName != "" and userprofile.lastFMPass != "":
                    scrobbler.login(userprofile.lastFMName,
                                    userprofile.lastFMPass,
                                    service="lastfm"
                                    )
                    scrobbler.submit(song.artist, song.title, now, source='P',
                                    length=song.length)
                    scrobbler.flush()
                    msg += "Scroblled song to lastfm! "
                    success = 1
        # if something bad happens, just ignore it
        except (scrobbler.BackendError, scrobbler.AuthError,
                scrobbler.PostError, scrobbler.SessionError,
                scrobbler.ProtocolError):
            success = 0
            
        # check for libre.fm scrobbling
        try:
            if request.user.get_profile().libreFMSubmit:
                if userprofile.libreFMName != "" and userprofile.libreFMPass != "":
                    scrobbler.login(userprofile.libreFMName,
                                    userprofile.libreFMPass,
                                    service="librefm"
                                    )
                    scrobbler.submit(song.artist, song.title, now, source='P',
                                    length=song.length)
                    scrobbler.flush()
                    msg += "Scroblled song to librefm!"
                    success = 1
        except (scrobbler.BackendError, scrobbler.AuthError,
                scrobbler.PostError, scrobbler.SessionError,
                scrobbler.ProtocolError):
            success = 0
    ctx = {
        'msg': msg,
        'success': success,
    }
    return render(request, 'ajax/success.json', ctx)


@check_login('user')
def ajax_song_cover(request):
    """Fetches the URL of albumcover, either locally or from the Internet

    Keyword arguments:
    id -- the id of the song we want the cover from
    """
    id = request.GET.get('id', '')
    song = get_object_or_404(Song, id=id)
    fetcher = CoverFetcher(song, request)
    cover = fetcher.fetch()
    ctx = {
        'coverpath': cover, 
        'album': song.album,
    }
    return render(request, 'ajax/cover.json', ctx)


@check_login('user')
def ajax_song_file(request):
    """
    Returns the audio file
    """
    id = request.GET.get('id', '')
    song = get_object_or_404(Song, id=id)
    return send_file(request, song.path)


@check_login("user")
def ajax_song_download(request):
    """
    Returns the audio file
    """
    id = request.GET.get('id', '')
    song = get_object_or_404(Song, id=id)
    return download_file(request, song)    


@check_login("user")
def ajax_playlist_list(request):
    """
    Returns all playlists of a user
    """
    playlists = Playlist.objects.filter(user=request.user)
    ctx = {
        'playlists': playlists
    }
    return render(request, 'ajax/playlists.html', ctx) 
    
    
@check_login("user")
def ajax_playlist_load(request):
    """
    Returns all entries of a playlist
    """
    name = request.POST.get('name', '')
    playlist = get_object_or_404(Playlist, user=request.user, name=name)
    songs = playlist.songs.all()
    ctx = {
        'playlist': playlist,
        'songs': songs
    }
    return render(request, 'ajax/playlist_songs.html', ctx) 


@check_login("user")
def ajax_playlist_save(request):
    """
    Returns all playlists of a user
    """
    success = 0
    msg = ""
    ctx = {
        'success': success,
        'msg': msg
    }
    return render(request, 'ajax/success.json', ctx) 
