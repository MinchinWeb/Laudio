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
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SetupForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), required=True, widget=forms.PasswordInput) 
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'last_login',
                   'date_joined', 'groups', 'user_permissions', 'password', 
                   'is_active', 'is_superuser')
