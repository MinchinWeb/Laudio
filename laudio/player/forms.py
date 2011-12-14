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
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Laudio imports
from laudio.player.models import UserProfile, XMLAPIUser
from laudio.src.inc.config import LaudioConfig


class SetupForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput) 
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password', 
                   'is_active', 'is_superuser')


class XMLAPIUserForm(forms.ModelForm):
    class Meta:
        model = XMLAPIUser
        widgets = {
            'password': forms.PasswordInput(render_value=False),
        }
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user')
        widgets = {
            'lastFMPass': forms.PasswordInput(render_value=False),
            'libreFMPass': forms.PasswordInput(render_value=False),
        }


class UserForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label=_('Superuser'),
        help_text=_('Sets if the user is a superuser. If a superuser exists, \
                    only superusers can view the settings dialogue'), required=False)
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password')


class UserEditForm(forms.ModelForm):
    is_superuser = forms.BooleanField(label=_('Superuser'),
        help_text=_('Sets if the user is a superuser. If a superuser exists, \
                    only superusers can view the settings dialogue'))
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password',
                   'username')


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password',
                   'username', 'is_active', 'is_superuser')


class SettingsForm(forms.ModelForm):
    collection_path = forms.CharField(label=_('Path to music collection'),
        help_text=_('Enter the path to your music collection, which you want to \
                    scan. Remember, all folders above the collection need to be \
                    executeable for the server user (normally www-data) and all \
                    music files need to be readable for the server user'))
    collection_startup = forms.BooleanField(required=False, label=_('Load songs on startup'),
        help_text=_('Automatically loads all songs in the player view. Dont check \
                    this checkbox if youve got more than 10k songs for it will \
                    remarkably slow down your browser'))
    require_login = forms.BooleanField(required=False, label=_('Require login'),
        help_text=_('Requires all users to log in to listen to your music'))
    xml_auth = forms.BooleanField(required=False, label=_('Enable Ampache XML API'),
        help_text=_('Enable the XML API to be able to listen to l-audio shares \
                    from other players like Amarok'))
    debug = forms.BooleanField(required=False, label=_('Debugging'),
        help_text=_('Activates debugging (Writes detailed logs and activates the \
                    Flash debug pluging)'))
    
    def clean_collection(self):
        """We move down folder by folder from the given path and check,
        if we can cd into the folder (we need a+x to cd into it).
        If we get any errors, we stop and tell the user to execute the right
        commands."""
        data = self.cleaned_data['collection_path']

        checkPath = data.split('/')
        checkedPath = ''
        for p in checkPath:            
            # if path is empty check the next element
            # concerns the first and last slash
            if not p:
                continue
            checkedPath += '/' + p
            
            # check for path existence and access rights
            if not os.access(checkedPath, os.F_OK):
                raise forms.ValidationError( 'Path %(path)s does not exist!' % {'path': checkedPath} )
            if not os.access(checkedPath, os.X_OK):
                raise forms.ValidationError( 'No access rights for %(path)s!'  % {'path': checkedPath} )
                
        # now check if we got read rights on the music folder, we could do this
        # recursively to check every folder but that would waste too mucht time
        if not os.access(data, os.R_OK):
            raise forms.ValidationError(_('Music collection is not readable!'))

        return data
    
    
    def save(self):
        """Saves the values into the config file
        """
        config = LaudioConfig(settings.LAUDIO_CFG)
        config.collection_path = self.cleaned_data['collection_path']
        config.debug = self.cleaned_data['debug']
        config.collection_startup = self.cleaned_data['collection_startup']
        config.require_login = self.cleaned_data['require_login']
        config.xml_auth = self.cleaned_data['xml_auth']
        config.save()
