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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

"""

# Django imports
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper


"""Keep your usefull tools here
"""

def render(request, tpl, tplvars={}):
    """Shortcut for renewing csrf cookie and passing request context
    
    Keyword arguments:
    tpl -- the template we want to use
    args -- the template variables

    """
    tplvars.update(csrf(request))
    # check config vars
    try:
        config = Settings.objects.get(pk=1)
        tplvars["audio_debug"] = config.debugAudio
        if request.user.is_authenticated():
            tplvars["auto_load"] = request.user.get_profile().showLib
            tplvars["hide_playlist"] = request.user.get_profile().hidePlaylist
            tplvars["hide_sidebar"] = request.user.get_profile().hideSidebar
        else:
            tplvars["auto_load"] = config.showLib
            tplvars["hide_playlist"] = config.hidePlaylist
            tplvars["hide_sidebar"] = config.hideSidebar
    except Settings.DoesNotExist, AttributeError:
        tplvars["audio_debug"] = False 
        tplvars["auto_load"] = False 
        tplvars["hide_playlist"] = False 
        tplvars["hide_sidebar"] = False 

    return render_to_response(tpl, tplvars,
                               context_instance=RequestContext(request))
                               
                               

def send_file(request, path):
    """                                                                         
    Send a file    
    
    Keyword arguments:
    download -- the path to the file
                                              
    """
    filename = os.path.basename(path).replace(" ", "_")                            
    wrapper = FileWrapper(file(path))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Disposition'] = u'attachment; filename=%s' % filename
    response['Content-Length'] = os.path.getsize(path)
    return response
    #return HttpResponse(filename)
