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
from django.conf import settings 
from django.conf.urls.defaults import *

urlpatterns = patterns('laudio.player.settings.views',
    # settings and profile
    url(r'^config/settings/$', 'config_settings', name='config_settings'),
    url(r'^config/profile/$', 'config_profile', name='config_profile'),
    url(r'^config/settings/new/user/$', 'config_settings_new_user', name='config_settings_new_user'),
    url(r'^config/settings/edit/user/(?P<userid>\d+)/$', 'config_settings_edit_user', name='config_settings_edit_user'),
    url(r'^config/settings/delete/user/(?P<userid>\d+)/$', 'config_settings_delete_user', name='config_settings_delete_user'),
    url(r'^config/settings/new/theme/$', 'config_settings_new_theme', name='config_settings_new_theme'),
    url(r'^config/settings/delete/theme/(?P<themename>\w+)/$', 'config_settings_delete_theme', name='config_settings_delete_theme'),
    url(r'^config/settings/xml/new/user/$', 'xml_config_settings_new_user', name='xml_config_settings_new_user'),
    url(r'^config/settings/xml/edit/user/(?P<userid>\d+)/$', 'xml_config_settings_edit_user', name='xml_config_settings_edit_user'),
    url(r'^config/settings/xml/delete/user/(?P<userid>\d+)/$', 'xml_config_settings_delete_user', name='xml_config_settings_delete_user'),
)
