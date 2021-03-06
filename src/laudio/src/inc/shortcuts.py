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
import urllib, urllib2
import os
import mimetypes

# Django imports
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.encoding import smart_str

# Laudio imports
from laudio.src.inc.config import LaudioConfig

"""Keep your usefull tools here
"""

def render(request, tpl, tplvars={}):
    """Shortcut for renewing csrf cookie and passing request context
    
    Keyword arguments:
    tpl -- the template we want to use
    args -- the template variables

    """
    tplvars.update(csrf(request))
    # pass config vars
    tplvars['config'] = LaudioConfig(settings.LAUDIO_CFG)
    tplvars['index_view'] = reverse('player:index')
    return render_to_response(tpl, tplvars,
                               context_instance=RequestContext(request))
                               
                               

def send_file(request, path):
    """                                                                         
    Send a file    
    
    Keyword arguments:
    request -- the request object
    path -- the path to the file
    """                         
    # FIXME: This is a piece of shit that does not properly serve html5 audio
    # media, i got frustrated, please someone else fix this
    mime = mimetypes.guess_type(path)[0]
    size = os.path.getsize(path)
    response = HttpResponse(content_type=mime)
    response['Content-Length'] = size
    response['X-Sendfile'] = smart_str(path)
    # Accept ranges are needed to make media seekable
    response['Accept-Ranges'] = 'bytes'
    return response
    

def download_file(request, song):
    """                                                                         
    Downloads a file
    
    Keyword arguments:
    request -- the request object
    song -- the song object
    """
    mime = mimetypes.guess_type(song.path)[0]
    size = os.path.getsize(song.path)
    wrapper = FileWrapper(file(song.path))
    response = HttpResponse(wrapper, content_type=mime)
    response['Content-Length'] = size
    filename = '%i %s - %s' % (song.tracknumber, song.artist, song.title)
    response['Content-Disposition'] = u'attachment; filename=%s' % filename.replace(' ', '_')
    return response
    
    
def get_var(request, name):
    """Gets and returns a GET variable escaped from the request 
    
    Keyword arguments:
    request -- The request
    """
    return urllib.unquote_plus(request.GET.get(name, ''))
    

def post_var(request, name):
    """Gets and returns a POST variable escaped from the request 
    
    Keyword arguments:
    request -- The request
    """
    return urllib.unquote_plus(request.POST.get(name, ''))
    
    
def handle_uploaded_file(f, dest_path):
    """Writes a file from one path to another path
    
    Keyword arguments:
    f -- The file object
    dest_path -- The path where you want to upload it to
    """
    destination = open(dest_path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
