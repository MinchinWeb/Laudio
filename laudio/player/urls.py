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

# main views
urlpatterns = patterns('laudio.player.views.player',
    url(r'^$', 'index', name='index'),
    url(r'^setup/$', 'setup', name='setup'),
    url(r'javascript/(?P<src>\w+)/$', 'javascript', name='javascript'),
    url(r'^logout/$', 'log_me_out', name='logout'),
)

# ajax views
urlpatterns += patterns('laudio.player.views.ajax', 
    # scan
    url(r'^ajax/scan/$', 'ajax_scan', name='ajax_scan'),
    url(r'^ajax/scan/progress/$', 'ajax_scan_progress', name='ajax_scan_progress'),
    # database
    url(r'^ajax/db/reset/$', 'ajax_db_reset', name='ajax_db_reset'),
    url(r'^ajax/db/rmnonexist/$', 'ajax_db_rmnonexist', name='ajax_db_rmnonexist'),
    url(r'^ajax/db/statistics/$', 'ajax_db_statistics', name='ajax_db_statistics'),
    # search
    url(r'^ajax/search/$', 'ajax_search', name='ajax_search'),
    url(r'^ajax/search/artist/letter/$', 'ajax_search_artist_letter', name='ajax_search_artist_letter'),
    # song data
    url(r'^ajax/song/data/$', 'ajax_song_data', name='ajax_song_data'),
    url(r'^ajax/song/file/$', 'ajax_song_file', name='ajax_song_file'),
    url(r'^ajax/song/download/$', 'ajax_song_download', name='ajax_song_download'),
    url(r'^ajax/song/scrobble/$', 'ajax_song_scrobble', name='ajax_song_scrobble'),
    url(r'^ajax/song/cover/$', 'ajax_song_cover', name='ajax_song_cover'),
)

# settings/config views
urlpatterns += patterns('laudio.player.views.config',
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

# xml views
urlpatterns += patterns('laudio.player.views.xml',
    url(r'^server/xml.server.php$', 'xml_api', name='xml_api'),
)

# built in views
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'config/login.html'}, name='login'),
)

