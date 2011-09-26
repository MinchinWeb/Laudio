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



# Django imports 
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse

# Laudio imports 
from laudio.inc.shortcuts import render
from laudio.inc.debugger import LaudioDebugger
import laudio.src.song.scrobbler as scrobbler
from laudio.src.song.coverfetcher import CoverFetcher
from laudio.inc.decorators import check_login
from laudio.inc.config import LaudioConfig
from laudio.player.models import *



########################################################################
# AJAX Requests                                                        #
########################################################################
@check_login("admin")
def settings_db_reset(request):
    """Deletes all playlists and songs in the db"""
    debug = LaudioDebugger()
    debug.log("Settings", "Attempting to delete playlists and songs")

    Song.objects.all().delete()
    Playlist.objects.all().delete()
    
    debug.log("Settings", "Deleted playlist and songs")
    return HttpResponse()


@check_login("admin")
def settings_db_scan_info(request):
    """gets the last scan entry and the scan values"""
    f = open(settings.SCAN_LOG, 'r')
    data = f.read()
    f.close()
    try:
        data = data.split(" ")
        scanned = data[0]
        total = data[1]
    except IndexError:
        scanned = 0
        total = 1
    return render_to_response('requests/scan_info.html', {"scanned": scanned,
                                                          "total": total })

@check_login("admin")
def settings_db_scan(request):
    """Scan the files in the collection"""
    config = LaudioSettings()
    try:
        config.scan()
    except OSError, e:
        return render_to_response( 'requests/dropscan.html', {"msg": e } )
    return render_to_response('requests/dropscan.html', { "msg": config.log })



