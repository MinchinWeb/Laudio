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
import os
import tarfile
import shutil

# Django imports
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings 
from django.views.i18n import set_language

# Laudio imports
from laudio.src.inc.shortcuts import render as csrf_render
from laudio.src.inc.decorators import check_login
from laudio.src.inc.resource_checker import ResourceChecker
from laudio.src.inc.config import LaudioConfig
from laudio.src.inc.debugger import LaudioDebugger
from laudio.player.models import XMLAPIUser
from laudio.player.forms import UserProfileForm, UserForm, SettingsForm, \
    UserEditProfileForm, UserEditForm, XMLAPIUserForm, ThemeForm, XMLAPIUserEditForm


@check_login('admin')
def config_settings(request):
    """The settings view
    """
    # get all files in the themepath that are folders
    themes = []
    themepath = os.path.join(settings.MEDIA_ROOT, 'themes/')
    for entry in os.listdir( themepath ):
        path = os.path.join(themepath, entry)
        if os.path.isdir( path ):
            themes.append(entry)
    
    users = User.objects.all()
    xml_users = XMLAPIUser.objects.all()
    warnings = ResourceChecker().get_warnings()
    
    # get form
    if request.method == 'POST':
        settings_form = SettingsForm(request.POST)
        if settings_form.is_valid():
            settings_form.save()
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'settings_form': settings_form,
            'users': users, 
            'xml_users': xml_users,
            'themes': themes,
            'warnings': warnings
        }
        return csrf_render(request, 'config/settings.html', ctx)
    else:
        config = LaudioConfig(settings.LAUDIO_CFG)
        initial = {
            'transcoding': config.transcoding,
            'collection_path': config.collectionPath,
            'debug': config.debug,
            'require_login': config.requireLogin,
            'collection_startup': config.collectionStartup, 
            'xml_auth': config.xmlAuth,
            'token_lifespan': config.tokenLifespan
        }
        settings_form = SettingsForm(initial=initial)    
        ctx = {
            'settings_form': settings_form,
            'users': users, 
            'xml_users': xml_users,
            'themes': themes,
            'warnings': warnings
        }
        return csrf_render(request, 'config/settings.html', ctx)

@check_login('admin')
def config_settings_new_user(request):
    """The settings view for creating a new user
    """
    # get form
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save(commit=False)
            profile_form.user = user.id
            profile_form.save()
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'config/settings_new_user.html', ctx)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()   
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'config/settings_new_user.html', ctx)
    

@check_login('admin')    
def config_settings_edit_user(request, userid):
    """The settings view for editing a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    # get form
    if request.method == 'POST':
        user = get_object_or_404(User, id=userid)
        user_profile = user.get_profile()
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save(commit=False)
            profile_form.user = User.objects.get(username=user_form.username)
            profile_form.save()
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form,
            'config_user': user
        }
        return csrf_render(request, 'config/settings_edit_user.html', ctx)
    else:
        user = get_object_or_404(User, id=userid)
        user_profile = user.get_profile()
        user_form = UserEditForm(instance=user)
        profile_form = UserEditProfileForm(instance=user_profile)    
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form,
            'config_user': user
        }
        return csrf_render(request, 'config/settings_edit_user.html', ctx)


@check_login('admin')
def config_settings_delete_user(request, userid):
    """The settings view for deleting a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    user = get_object_or_404(User, id=userid)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('player:config_settings'))
    else:
        ctx = {
            'change_user': user
        }
        return csrf_render(request, 'config/settings_delete_user.html', ctx)


@check_login('admin')
def xml_config_settings_new_user(request):
    """The settings view for creating a new xml api user
    """
    # get form
    if request.method == 'POST':
        user_form = XMLAPIUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'user_form': user_form
        }
        return csrf_render(request, 'config/xml_settings_new_user.html', ctx)
    else:
        user_form = XMLAPIUserForm()
        ctx = {
            'user_form': user_form
        }
        return csrf_render(request, 'config/xml_settings_new_user.html', ctx)
    

@check_login('admin')    
def xml_config_settings_edit_user(request, userid):
    """The settings view for editing a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    # get form
    if request.method == 'POST':
        user = get_object_or_404(XMLAPIUser, id=userid)
        user_form = XMLAPIUserEditForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'user_form': user_form,
            'config_user': user
        }
        return csrf_render(request, 'config/xml_settings_edit_user.html', ctx)
    else:
        user = get_object_or_404(XMLAPIUser, id=userid)
        user_form = XMLAPIUserEditForm(instance=user)
        ctx = {
            'user_form': user_form,
            'config_user': user
        }
        return csrf_render(request, 'config/xml_settings_edit_user.html', ctx)


@check_login('admin')
def xml_config_settings_delete_user(request, userid):
    """The settings view for deleting a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    user = get_object_or_404(XMLAPIUser, id=userid)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('player:config_settings'))
    else:
        ctx = {
            'change_user': user
        }
        return csrf_render(request, 'config/xml_settings_delete_user.html', ctx)


@check_login('admin')
def config_settings_new_theme(request):
    """The settings view for creating a new xml api user
    """
    # get form
    debug = LaudioDebugger()
    if request.method == 'POST':
        theme_form = ThemeForm(request.POST, request.FILES)
        if theme_form.is_valid():
            try:
                theme_form.install_theme(request.FILES['theme'])
            except (tarfile.CompressionError, tarfile.ReadError, TypeError), msg:
                debug.log('Theme Upload', msg)
            return HttpResponseRedirect(reverse('player:config_settings'))
        ctx = {
            'theme_form': theme_form
        }
        return csrf_render(request, 'config/settings_new_theme.html', ctx)
    else:
        theme_form = ThemeForm()
        ctx = {
            'theme_form': theme_form
        }
        return csrf_render(request, 'config/settings_new_theme.html', ctx)


@check_login('admin')
def config_settings_delete_theme(request, themename):
    """The settings view for deleting a user
    
    Keyword arguments:
    userid -- The id of the user
    """
    if request.method == 'POST':
        # todo unlink theme
        if themename != 'default':
            themes_dir = os.path.join(settings.MEDIA_ROOT, 'themes/')
            theme_path = os.path.join(themes_dir, themename)
            shutil.rmtree(theme_path)
        else:
            debug = LaudioDebugger()
            debug.log('Theme Deletion', 'Can not delete default theme')
        return HttpResponseRedirect(reverse('player:config_settings'))
    else:
        ctx = {
            'themename': themename
        }
        return csrf_render(request, 'config/settings_delete_theme.html', ctx)


@check_login('user')
def config_profile(request):
    """The profile view
    """    
    # get form
    if request.method == 'POST':
        user = request.user
        user_profile = request.user.get_profile()
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserEditProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            set_language(request)
            return HttpResponseRedirect(reverse('player:config_profile'))
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'config/profile.html', ctx)
    else:
        user = request.user
        user_profile = request.user.get_profile()
        user_form = UserEditForm(instance=user)
        profile_form = UserEditProfileForm(instance=user_profile)    
        ctx = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return csrf_render(request, 'config/profile.html', ctx)
        

