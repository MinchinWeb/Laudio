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
from django.contrib.auth import logout
from django.conf import settings

# Project imports
from laudio.src.inc.shortcuts import render as csrf_render
from laudio.player.forms import SetupForm
from laudio.src.inc.decorators import check_login
from laudio.player.models import UserProfile, Artist, Album, Genre
from laudio.src.inc.config import LaudioConfig

def index(request):
    """
    Main view for the application
    """
    # check if we have to create a superuser
    su_exists = len(User.objects.filter(is_superuser=True))
    if not su_exists:
        return HttpResponseRedirect( reverse('player:setup') )
    else:
        return player(request)
    return player(request)


@check_login('user') 
def player(request):
    """Shows the player if there are superusers
    """
    artists = Artist.objects.all().distinct('name').order_by('name')
    albums = Album.objects.all().distinct('name').order_by('name')
    genres = Genre.objects.all().distinct('name').order_by('name')
    ctx = {
        'artists': artists,
        'albums': albums,
        'genres': genres
    }
    return csrf_render(request, 'player/index.html', ctx)
    
    
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
                userform = form.save(commit=False)
                userform.is_active = True
                userform.is_superuser = True
                userform.is_staff = True
                userform.save()
                # create a profile
                profile = UserProfile()
                profile.user = User.objects.get(username=userform.username)
                profile.save()
                return HttpResponseRedirect(reverse('player:index'))
        ctx = {
            'form': form,
        }
        return csrf_render(request, 'install/index.html', ctx)
    else:
        raise Http404
        

def javascript(request, src):
    """Generates the javascript from templates

    Keyword arguments:
    src -- The javascript part which should be generated 
    """
    tpl = ''
    ctx = {
        'config': LaudioConfig(settings.LAUDIO_CFG)
    }
    if src == 'main':
        tpl = 'javascript/main.js'
    elif src == 'ui':
        tpl = 'javascript/ui.js'
    elif src == 'player':
        tpl = 'javascript/player.js'
    elif src == 'inc':
        tpl = 'javascript/inc.js'
    elif src == 'playlist':
        tpl = 'javascript/playlist.js'
    elif src == 'settings':
        tpl = 'javascript/settings.js'
    elif src == 'search':
        tpl = 'javascript/search.js'
        
    return render(request, tpl, ctx)


def log_me_out(request):
    """Simple logout view
    """
    logout(request)
    return HttpResponseRedirect( reverse('player:index') )

