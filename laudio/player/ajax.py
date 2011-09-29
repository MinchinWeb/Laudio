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
from django.utils.translation import ugettext as _

# Laudio imports 
from laudio.inc.shortcuts import render
from laudio.inc.debugger import LaudioDebugger
import laudio.src.song.scrobbler as scrobbler
from laudio.src.song.coverfetcher import CoverFetcher
from laudio.inc.decorators import check_login
from laudio.inc.config import LaudioConfig
from laudio.inc.scan_progress import ScanProgressor
from laudio.player.models import *



########################################################################
# AJAX Requests                                                        #
########################################################################
@check_login("admin")
def settings_db_reset(request):
    """Deletes all playlists and songs in the db"""
    # TODO: insert count of tracks and playlists that were
    #       deleted and which are left
    debug = LaudioDebugger()
    debug.log("Settings", "Attempting to delete playlists and songs")

    Song.objects.all().delete()
    Playlist.objects.all().delete()
    
    debug.log("Settings", "Deleted playlist and songs")
    
    return render(request, 'requests/success.xml', { 
                    "msg": _("Deleted all Playlists and songs"), 
                    "success": 1 
                 })


@check_login("admin")
def settings_db_scan_info(request):
    """gets the last scan entry and the scan values"""
    progress = ScanProgressor()
    scanned, total = progress.getScannedTracks()
    return render(request, 'requests/scan_count.xml', {"scanned": scanned,
                                                          "total": total })

@check_login("admin")
def settings_db_rm_nonexist(request):
    """Remove non existent files from the db"""
    config = LaudioConfig()
    scanner = MusicScanner()
    debug = LaudioDebugger()  
    debug.log("Settings", "Atempting to delete non existent tracks from the database")
    scanner.rmNonExist()
    return render(request, 'requests/success.xml', { 
                    "msg": _("Deleted non existent tracks in the database"), 
                    "success": 1 
                 })



@check_login("admin")
def settings_db_scan(request):
    """Scan the files in the collection"""
    config = LaudioConfig()
    progress = ScanProgressor()
    if not os.access(DATABASES['default']['NAME'], os.W_OK):
        msg = _("No write access to database: %(path)s") % {"path": settings.DATABASES['default']['NAME']}
        success = 0
    # check if scan is running
    elif progressor.isScanning():
        msg = _("Can not run scan because a scan is already being run")
        success = 0
    else:
        scanner = MusicScanner(config.collectionPath)
        scanner.scan()
        msg = _("Scanned %(number)i files") % {"number": scanner.scanned}
        msg += _("Updated %(number)i files") % {"number": scanner.modified}
        msg += _("Added %(number)i files") % {"number": scanner.added}
        for file in scanner.broken:
            msg += _("The file: %(path)s is broken") % {"path": file}
        for file in scanner.noRights:
            msg += _("The file: %(path)s is not accessible due to filerights") % {"path": file} 
        success = 1
    return render(request, 'requests/success.xml', { "msg": msg, "success": success })



