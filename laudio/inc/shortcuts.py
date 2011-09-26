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
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext

# Laudio imports
from laudio.inc.config import LaudioConfig

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
    tplvars["config"] = LaudioConfig()
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
