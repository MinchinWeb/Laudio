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

from django.conf import settings 
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class XMLAPIUser(models.Model):
    username = models.CharField(_('Username'), max_length=250, unique=True)
    password = models.CharField(_('Password'), max_length=64, blank=True)
    token = models.CharField(_('Token'), max_length=64)
    last_handshake = models.DateTimeField(_('Last handshake'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)
    is_active = models.BooleanField(_('Is active'), help_text=_('Set to true if \
            you want the user to be able to access the XML API'), blank=True,
            default=True)

    def set_password(self, password):
        self.password = hashlib.sha256(password)
