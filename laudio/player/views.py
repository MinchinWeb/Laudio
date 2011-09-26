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
from django.core.urlresolvers import reverse

# Laudio imports 
from laudio.inc.shortcuts import render
import laudio.src.song.scrobbler as scrobbler
from laudio.src.song.coverfetcher import CoverFetcher
# from laudio.src.javascript import JavaScript
from laudio.inc.decorators import check_login
from laudio.inc.config import LaudioConfig
from laudio.player.models import *
from laudio.player.forms import *


@check_login("user")
def index(request):
    """The collection view which is displayed as index by default
    
    If the directory is not set and thus you can't play songs, redirect
    to the settings page."""

    # Check if there are any superusers, otherwise redirect them
    # to the settings page to create one
    if User.objects.filter(is_superuser=1).count() == 0:
        return HttpResponseRedirect( reverse("player:settings") )

    config = LaudioConfig()
    # get javascript
    # js = JavaScript("library", request)
    js = ""
    
    # get number of songs
    count = Song.objects.aggregate( Sum("length") )
    mp3s = Song.objects.filter(codec="mp3").aggregate( Count("id") )["id__count"]
    oggs = Song.objects.filter(codec="ogg").aggregate( Count("id") )["id__count"]
    songs = mp3s + oggs 
    hours = 0 # int( count["length__sum"] / (60 * 60) )
    days = int( hours / 24 )
    weeks = int( days / 7 )
    
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
    config = LaudioConfig()
    
    if request.method == 'POST':
        settingsForm = SettingsForm(request.POST)
        if settingsForm.is_valid(): 
            fields = ("requireLogin", "debug", "collectionPath", 
                      "collectionStartup", "hideSidebar", "hidePlaylist",
                      "xmlAPIAuth")
            # write data config file
            for key in fields:
                setattr(config, key, settingsForm.cleaned_data[key])
            config.save()
    else:
        default_data = {
            "collectionPath": config.collectionPath,
            "debug": config.debug,
            "requireLogin": config.requireLogin,
            "collectionStartup": config.collectionStartup,
            "hideSidebar": config.hideSidebar,
            "hidePlaylist": config.hidePlaylist,
            "xmlAPIAuth": config.xmlAPIAuth,
        }
        settingsForm = SettingsForm(default_data)
            
    # js = JavaScript("settings", request)
    js = ""
    users = User.objects.all()

    return render(request, 'settings/settings.html', { 
                                                "collection": config.collectionPath,  
                                                "settingsForm": settingsForm,
                                                "users": users,
                                                "js": js, 
                                            }
                 )
                     
                            
@check_login("admin")    
def settings_user_new(request):
    """Create a new user"""
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        profileForm = UserProfileForm(request.POST)
        
        if userForm.is_valid() and profileForm.is_valid(): 
            user = userForm.save(commit=False)
            user.set_password( request.POST.get('password') )
            user.save()
            # profile
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect( reverse ("player:settings") )
    else:
        userForm = UserForm()
        profileForm = UserProfileForm()

    return render(request, 'settings/newuser.html', { "userform": userForm,  
                                                      "profileform": profileForm
                                                    }
                            )


@check_login("admin")
def settings_user_edit(request, userid):
    """Edit a user by userid"""
    if request.method == 'POST':
        userForm = UserEditForm(request.POST)
        profileForm = UserProfileForm(request.POST)
        
        if userForm.is_valid() and profileForm.is_valid(): 
            user = userForm.save(commit=False)
            if request.POST.get('password') != "":
                user.set_password( request.POST.get('password') )
            user.save()
            # profile
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect( reverse ("player:settings") )
    else:
        user = User.objects.get(pk=userid)
        userForm = UserEditForm(instance=user)
        profile = UserProfile.objects.get(user=user)
        profileForm = UserProfileForm(instance=profile)

    return render(request, 'settings/edituser.html', {"userform": userForm,  
                                                      "profileform": profileForm
                                                     }
                            )


@check_login("admin")
def settings_user_delete(request, userid):
    """Deletes a user by userid"""
    # FIXME: possible csrf vulnerability
    user = User.objects.get(pk=userid)
    user.delete()
    return HttpResponseRedirect( reverse ("player:settings") )
    
    
@check_login("user")
def profile(request):
    """Edit a profile"""
    user = request.user
    
    if request.method == 'POST':
        userForm = UserEditProfileForm(request.POST)
        profileForm = UserProfileForm(request.POST)
        
        if userForm.is_valid() and profileForm.is_valid(): 
            user.email = userForm.cleaned_data['email']
            if request.POST.get('password') != "":
                user.set_password( request.POST.get('password') )
            user.save()
            # profile
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect( reverse ("player:profile") )
    else:
        userForm = UserEditProfileForm(instance=user)
        profile = UserProfile.objects.get(user=user)
        profileForm = UserProfileForm(instance=profile)

    return render(request, 'profile.html', { "userform": userForm,  
                                             "profileform": profileForm
                                          }
                            )

def song_download(request):
    return HttpResponse("hi")
