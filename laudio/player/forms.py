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
import re

# Django imports
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Laudio imports
from laudio.player.models import UserProfile, XMLAPIUser
from laudio.src.inc.config import LaudioConfig
from laudio.src.inc.shortcuts import handle_uploaded_file


class SetupForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), required=True, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password', 
                   'is_active', 'is_superuser', 'email')
           
    def clean_password2(self):
        """Password confirmation checker
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """Sets the password for the user on save
        
        Keyword arguments:
        commit -- True if the values should be saved into the db
        """
        user = super(SetupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        

class XMLAPIUserForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), required=True, widget=forms.PasswordInput)
    
    class Meta:
        model = XMLAPIUser
        exclude = ('modified', 'token', 'last_handshake', 'password')
           
    def clean_password2(self):
        """Password confirmation checker
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """Sets the password for the user on save
        
        Keyword arguments:
        commit -- True if the values should be saved into the db
        """
        user = super(XMLAPIUserForm, self).save(commit=False)
        # dont save if the password is empty
        if self.cleaned_data["password1"] == '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class XMLAPIUserEditForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), required=False, widget=forms.PasswordInput)
    
    class Meta:
        model = XMLAPIUser
        exclude = ('modified', 'token', 'last_handshake', 'password')
           
    def clean_password2(self):
        """Password confirmation checker
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """Sets the password for the user on save
        
        Keyword arguments:
        commit -- True if the values should be saved into the db
        """
        user = super(XMLAPIUserEditForm, self).save(commit=False)
        # dont save if the password is empty
        if self.cleaned_data["password1"] == '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(label=_('Superuser'),
        help_text=_('Sets if the user is a superuser. If a superuser exists, \
                    only superusers can view the settings dialogue'), required=False)
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password')

    def clean_password2(self):
        """Password confirmation checker
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """Sets the password for the user on save
        
        Keyword arguments:
        commit -- True if the values should be saved into the db
        """
        user = super(UserForm, self).save(commit=False)
        # dont save password if the password field is empty
        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'), required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password',
                   'username', 'is_active', 'is_superuser')
                   
    def clean_password2(self):
        """Password confirmation checker
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """Sets the password for the user on save
        
        Keyword arguments:
        commit -- True if the values should be saved into the db
        """
        user = super(UserEditForm, self).save(commit=False)
        # dont save password if the password field is empty
        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class SettingsForm(forms.Form):
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
    token_lifespan = forms.IntegerField(label=_('Lifespan of the Ampache XML API Token in Seconds'),
        help_text=_('If the token expires, the application has to reidentify itself. \
                        Too short tokens will cause a lot of identifications, \
                        too long ones will weaken the security.'))
    transcoding = forms.BooleanField(required=False, label=_('Allow Transcoding'),
        help_text=_('Allows users to activated transcoding to a lower bitrate \
                    to save bandwidth. This may cause high CPU load'))
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
                raise forms.ValidationError( _('Path %(path)s does not exist!') % {'path': checkedPath} )
            if not os.access(checkedPath, os.X_OK):
                raise forms.ValidationError(  _('No access rights for %(path)s!')  % {'path': checkedPath} )
                
        # now check if we got read rights on the music folder, we could do this
        # recursively to check every folder but that would waste too mucht time
        if not os.access(data, os.R_OK):
            raise forms.ValidationError(_('Music collection is not readable!'))

        return data
    
    
    def save(self):
        """Saves the values into the config file
        """
        config = LaudioConfig(settings.LAUDIO_CFG)
        config.collectionPath = self.cleaned_data['collection_path']
        config.debug = self.cleaned_data['debug']
        config.collectionStartup = self.cleaned_data['collection_startup']
        config.requireLogin = self.cleaned_data['require_login']
        config.xmlAuth = self.cleaned_data['xml_auth']
        config.transcoding = self.cleaned_data['transcoding']
        config.tokenLifespan = self.cleaned_data['token_lifespan']
        config.save()


class ThemeForm(forms.Form):
    theme = forms.FileField()
    
    def install_theme(self, upload_file):
        """
        Checks if a the theme is already in the themepath or the 
        theme is called default
        
        Keyword arguments
        upload_file -- The upload file object which we get from request.FILES
        """
        name = upload_file.name
        upload_theme_path = os.path.join( settings.MEDIA_ROOT, 'themes/' )
        dest_name = '%s%s' % (upload_theme_path, name)
        
        # check if theres already a tar.gz file in the media with the same name
        # if so, just delete it
        if name in os.listdir( upload_theme_path ):
            os.unlink( dest_name )
        
        # move tar.gz to the theme folder
        handle_uploaded_file( upload_file, dest_name )

        # check if theres already a folder like in the tar.gz
        with tarfile.open(dest_name, 'r:*') as tar:
            for file in tar:
                # check if the themename overwrites the default theme which it 
                # must not
                topdir = file.name.split('/')[0]
                if topdir == 'default':
                    os.unlink(dest_name)
                    raise TypeError('Theme must not be name default')
                # check if the file contains invalid characters
                if re.search(r'[^\w]', topdir):
                    os.unlink(dest_name)
                    raise TypeError('Theme name contains illegal characters')
                # if themename is not default, remove the theme if its there
                if topdir in os.listdir( upload_theme_path ):
                    shutil.rmtree( os.path.join(upload_theme_path, topdir) )
        
            # finally extract the tar file
            tar.extractall(upload_theme_path)
        
        # delete remaining tar.gz file
        os.unlink(dest_name)
