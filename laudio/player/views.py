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
import os
import urllib
import urllib2

# Django imports 
from django.db.models import Q
from django.db.models import Count, Sum
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.core.urlresolvers import reverse

# Laudio imports 
import laudio.src.song.scrobbler as scrobbler
from laudio.src.song.coverfetcher import CoverFetcher
from laudio.src.javascript import JavaScript
from laudio.inc.decorators import check_login
from laudio.inc.config import LaudioConfig
from laudio.player.models import *
from laudio.player.forms import *


@check_login("user")
def index(request):
    """The collection view which is displayed as index by default
    
    If the directory is not set and thus you can't play songs, redirect
    to the settings page."""

    config = LaudioConfig()

    # get javascript
    js = JavaScript("library", request)
    
    # get number of songs
    count = Song.objects.aggregate( Count("id"), Sum("length") )
    mp3s = Song.objects.filter(codec="mp3").aggregate( Count("id") )
    oggs = Song.objects.filter(codec="ogg").aggregate( Count("id") )
    songs = count["id__count"]
    hours = int( count["length__sum"] / (60 * 60) )
    days = int( hours / 24 )
    weeks = int( days / 7 )
    mp3s = mp3s["id__count"]
    oggs = oggs["id__count"]
    return render(request, 'index.html', { 
                                            'js': js, 
                                            'numberOfSongs': songs,
                                            'numberOfMp3s': mp3s,
                                            'numberOfOggs': oggs,
                                            'numberOfHours': hours,
                                            'numberOfDays': days,
                                            'numberOfWeeks': weeks,
                                            }
                    )
                                
    
@check_login("admin")
def settings(request):
    """Site where the configuration happens"""
    config = LaudioSettings()
    users = User.objects.all()
    if request.method == 'POST':
        settingsForm = SettingsForm(request.POST)
        if settingsForm.is_valid(): 
            # get the first setting in the db
            try:
                settings = Settings.objects.get(pk=1)
            except Settings.DoesNotExist:
                settings = Settings()
            fields = ("requireLogin", "debugAudio", "collection", "showLib",
                      "hideSidebar", "hidePlaylist")
            # write data into db
            for key in fields:
                setattr(settings, key, settingsForm.cleaned_data[key])
            settings.save()
            # set symlink
            config.setCollectionPath(settingsForm.cleaned_data['collection'])
    else:
        try:
            settings = Settings.objects.get(pk=1)
            settingsForm = SettingsForm(instance=settings)
        except Settings.DoesNotExist:
            settingsForm = SettingsForm(initial={'cacheSize': 100})
            
    # get javascript
    js = JavaScript("settings", request)
    return render(request, 'settings/settings.html', { "collection": config.collectionPath,  
                                               "settingsForm": settingsForm,
                                               "users": users,
                                               "js": js, 
                                            }
                 )
                     
                            
@check_login("admin")    
def settings_user_new(request):
    """Create a new user"""
    if request.method == 'POST':
        userform = UserForm(request.POST)
        profileform = UserProfileForm(request.POST)
        
        if userform.is_valid() and profileform.is_valid(): 
            user = User(username=userform.cleaned_data['username'],
                        email=userform.cleaned_data['email'],
                        is_superuser=userform.cleaned_data['is_superuser'],
                        is_active=userform.cleaned_data['is_active'])
            user.set_password( request.POST.get('password') )
            user.save()
            # profile
            profile = UserProfile(user=user)
            for key in ("lastFMName", "lastFMPass", "lastFMSubmit", 
                         "libreFMName", "libreFMPass", "libreFMSubmit",
                         "hidePlaylist", "hideSidebar", "showLib"):
                setattr(profile, key, profileform.cleaned_data[key])
            profile.save()
            return HttpResponseRedirect( reverse ("laudio.views.laudio_settings") )
    else:
        userform = UserForm()
        profileform = UserProfileForm()

    return render(request, 'settings/newuser.html', { "userform": userform,  
                                                          "profileform": profileform
                                                        }
                            )


@check_login("admin")
def settings_user_edit(request, userid):
    """Edit a user by userid"""
    if request.method == 'POST':
        
        userform = UserEditForm(request.POST)
        profileform = UserProfileForm(request.POST)
        
        if userform.is_valid() and profileform.is_valid(): 
            user = User.objects.get(pk=userid)
            user.email = userform.cleaned_data['email']
            user.is_superuser = userform.cleaned_data['is_superuser']
            user.is_active = userform.cleaned_data['is_active']
            if request.POST.get('password') != "":
                user.set_password( request.POST.get('password') )
            user.save()
            # profile
            profile = UserProfile.objects.get(user=user)
            profile.user = user
            for key in ("lastFMName", "lastFMPass", "lastFMSubmit", 
                         "libreFMName", "libreFMPass", "libreFMSubmit",
                         "hidePlaylist", "hideSidebar", "showLib"):
                setattr(profile, key, profileform.cleaned_data[key])
            profile.save()
            return HttpResponseRedirect( reverse ("laudio.views.laudio_settings") )
    else:
        user = User.objects.get(pk=userid)
        userform = UserEditForm(instance=user)
        profile = UserProfile.objects.get(user=user)
        profileform = UserProfileForm(instance=profile)

    return render(request, 'settings/edituser.html', { "userform": userform,  
                                                          "profileform": profileform
                                                        }
                            )


@check_login("admin")
def settings_user_delete(request, userid):
    """Deletes a user by userid"""
    # FIXME: possible csrf vulnerability
    user = User.objects.get(pk=userid)
    user.delete()
    return HttpResponseRedirect( reverse ("laudio.views.laudio_settings") )
    
    
@check_login("user")
def profile(request):
    """Edit a profile"""
    user = request.user
    
    if request.method == 'POST':
        userform = UserEditProfileForm(request.POST)
        profileform = UserProfileForm(request.POST)
        
        if userform.is_valid() and profileform.is_valid(): 
            user.email = userform.cleaned_data['email']
            if request.POST.get('password') != "":
                user.set_password( request.POST.get('password') )
            user.save()
            # profile
            profile = UserProfile.objects.get(user=user)
            profile.user = user
            for key in ("lastFMName", "lastFMPass", "lastFMSubmit", 
                         "libreFMName", "libreFMPass", "libreFMSubmit",
                         "hidePlaylist", "hideSidebar", "showLib"):
                setattr(profile, key, profileform.cleaned_data[key])
            profile.save()
            return HttpResponseRedirect( reverse ("laudio.views.laudio_profile") )
    else:
        
        userform = UserEditProfileForm(instance=user)
        profile = UserProfile.objects.get(user=user)
        profileform = UserProfileForm(instance=profile)

    return render(request, 'settings/profile.html', { "userform": userform,  
                                                          "profileform": profileform
                                                        }
                            )

