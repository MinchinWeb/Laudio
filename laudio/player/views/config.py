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
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

# Laudio imports
from laudio.src.inc.shortcuts import render as csrf_render
from laudio.src.inc.decorators import check_login
from laudio.player.forms import UserProfileForm, UserForm, SettingsForm

@check_login('admin')
def config_settings(request):
    """The settings view
    """
    ctx = {}
    return csrf_render(request, 'config/settings.html', ctx)


@check_login('admin')
def config_settings_new_user(request, userid):
    """The settings view for creating a new user
    """
    ctx = {}
    return csrf_render(request, 'config/settings_new_user.html', ctx)
    

@check_login('admin')    
def config_settings_edit_user(request, userid):
    """The settings view for editing a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    ctx = {}
    return csrf_render(request, 'config/settings_edit_user.html', ctx)


@check_login('admin')
@require_POST
def config_settings_delete_user(request, userid):
    """The settings view for deleting a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    ctx = {}
    return csrf_render(request, 'config/settings_delete_user.html', ctx)


@check_login('admin')
def xml_config_settings_new_user(request, userid):
    """The settings view for creating a new user
    """
    ctx = {}
    return csrf_render(request, 'config/xml_settings_new_user.html', ctx)
    

@check_login('admin')    
def xml_config_settings_edit_user(request, userid):
    """The settings view for editing a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    ctx = {}
    return csrf_render(request, 'config/xml_settings_edit_user.html', ctx)


@check_login('admin')
@require_POST
def xml_config_settings_delete_user(request, userid):
    """The settings view for deleting a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    ctx = {}
    return csrf_render(request, 'config/xml_settings_delete_user.html', ctx)


@check_login('user')
def config_profile(request):
    """The profile view
    """    
    # get form
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('player:config_profile'))
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'config/profile.html', ctx)
    else:
        user = request.user
        user_profile = request.user.get_profile()
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)    
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'config/profile.html', ctx)
        

@check_login('admin')
def config_settings(request):
    """The profile view
    """    
    # get form
    if request.method == 'POST':
        settings_form = SettingsForm(request.POST)
        if settings_form.is_valid():
            settings_form.save()
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'settings_form': settings_form
        }
        return csrf_render(request, 'config/settings.html', ctx)
    else:
        settings_form = SettingsForm()    
        ctx = {
            'settings_form': settings_form
        }
        return csrf_render(request, 'config/settings.html', ctx)
