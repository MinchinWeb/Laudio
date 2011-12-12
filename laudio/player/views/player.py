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
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

# Project imports
from laudio.src.inc.shortcuts import render as csrf_render
from laudio.player.forms import SetupForm
from laudio.src.inc.decorators import check_login



def index(request):
    """
    Main view for the application
    """
    # check if we have to create a superuser
    #su_exists = len(User.objects.filter(is_superuser=True))
    #if not su_exists:
    #    return HttpResponseRedirect( reverse('player:setup') )
    #else:
    #    return player(request)
    return player(request)


@check_login('user') 
def player(request):
    """Shows the player if there are superusers
    """
    return csrf_render(request, 'player/index.html')
    
    
def setup(request):
    """Setup view
    """
    su_exists = len(User.objects.filter(is_superuser=True))
    if not su_exists:
        form = SetupForm()
        # get form
        if request.method == 'POST':
            form = SetupForm(request.POST)
            if form.is_valid():
                upload = form.save(commit=False)
                upload.is_active = True
                upload.is_superuser = True
                upload.is_staff = True
                upload.save()
                # FIXME: check if pass is set correctly
                User.objects.get(id=upload.id).set_password(request.POST.get('password', ''))
                return HttpResponseRedirect(revers('player:index'))
        ctx = {
            "form": form,
        }
        return csrf_render(request, 'install/index.html', ctx)
    else:
        raise Http404
        

def javascript(request, src):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    if src == 'main':
        tpl = 'javascript/main.js'
    elif src == 'ui':
        tpl = 'javascript/ui.js'
    elif src == 'player':
        tpl = 'javascript/player.js'
    elif src == 'inc':
        tpl = 'javascript/inc.js'

    return render(request, tpl)
