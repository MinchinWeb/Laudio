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

# Django imports
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Laudio imports
from laudio.player.models import *


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user")
        widgets = {
            'lastFMPass': forms.PasswordInput(render_value=False),
            'libreFMPass': forms.PasswordInput(render_value=False),
        }


class UserForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label=_("Superuser"), 
        help_text=_("Sets if the user is a superuser. If a superuser exists, \
        only superusers can view the settings dialogue"), required=False)
    class Meta:
        model = User
        exclude = ("first_name", "last_name", "is_staff", "last_login", 
                   "date_joined", "groups", "user_permissions", "password")

class UserEditForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label=_("Superuser"), 
        help_text=_("Sets if the user is a superuser. If a superuser exists, \
        only superusers can view the settings dialogue"))
    class Meta:
        model = User
        exclude = ("first_name", "last_name", "is_staff", "last_login", 
                   "date_joined", "groups", "user_permissions", "password",
                   "username")

class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ("first_name", "last_name", "is_staff", "last_login", 
                   "date_joined", "groups", "user_permissions", "password",
                   "username", "is_active", "is_superuser")


class SettingsForm(forms.Form):
    collectionPath = forms.CharField(label=_("Collection Path"), required=True,
        help_text=_("Sets ONLY the path to your music files! To add the \
        files to your library hit the \"Scan collection\" \
        button button above. All directories above the music \
        directory need to have the rights a+x, all music files \
        need to be 0755"))
    requireLogin  = forms.BooleanField(label=_("Require Login"), required=False,
        help_text=_("All users who want to listen to your files have to log in"))
    collectionStartup = forms.BooleanField(label=_("Load collection"), required=False,
        help_text=_("This displays your whole collection automatically on startup. \
        Be carefull with bigger collections as it may impact your \
        browser's speed"))
    debug = forms.BooleanField(label=_("Debug"), required=False,
        help_text=_("Enable output to your firebug console including audio debug information \
        and writing of debug information while scanning your collection \
        to %(debug_log_path)s") % {"debug_log_path": settings.DEBUG_LOG} )
    hidePlaylist = forms.BooleanField(label=_("Hide playlist by default"), 
        help_text=_("Automatically \
        hides the playlist in the Collection view so you have \
        to click playlist to view it"), required=False)
    hideSidebar = forms.BooleanField(label=_("Hide sidebar by default"), 
        help_text=_("Automatically \
        hides the sidebar in the Collection view so you have \
        to click sidebar to view it"), required=False)
    xmlAPIAuth = forms.BooleanField(label=_("Enable experimental XML API"), 
        help_text=_("Any program which wishes to access your data has \
        can access your data and songs, even if you have set Laudio to \
        require login. NO AUTHENTICATION IS NEEDED!"),
        required=False)
        

    def clean_collectionPath(self):
        data = self.cleaned_data['collectionPath']
        """We move down folder by folder from the given path and check,
        if we can cd into the folder (we need a+x to cd into it).
        If we get any errors, we stop and tell the user to execute the right
        commands."""
        
        # TODO: check cmds!
        checkPath = data.split("/")
        checkedPath = ""
        for p in checkPath:
            
            # if path is empty check the next element
            # concerns the first and last slash
            if not p:
                continue
            checkedPath += "/" + p
            
            # check for path existence and access rights
            if not os.access(checkedPath, os.F_OK):
                raise forms.ValidationError( _("Path %(file_path)s does not exist!") % {"file_path" % checkedPath})
            if not os.access(checkedPath, os.X_OK):
                raise forms.ValidationError( _("No access rights for %(path)s! Use: <b>sudo \
                        chmod a+x %(path_cmd)s</b>") % {"path": checkedPath, "path_cmd": checkedPath} )
                
        """now check if we got read rights on the music folder, we could do this
        recursively to check every folder but that would waste too mucht time"""
        if not os.access(data, os.R_OK):
            raise forms.ValidationError( "Music collection is not readable! Use: <b>sudo chmod \
                           -R 0755 %(path)s</b>" % {"path": data} )

        return data
