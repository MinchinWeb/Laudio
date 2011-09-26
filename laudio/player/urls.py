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
from django.conf import settings as django_settings
from django.conf.urls.defaults import *

# Laudio imports
from laudio.player.views import *
from laudio.player.xml_api import *
#from laudio.player.ajax import *

urlpatterns = patterns('',
    
    # Settings
    url(r'^settings/$', settings, name='settings'),
    url(r'^settings/user/new/$', settings_user_new, name='settings_user_new'),
    url(r'^settings/user/delete/(?P<userid>.*)/$', settings_user_delete, name='settings_user_delete'),
    url(r'^settings/user/edit/(?P<userid>.*)/$', settings_user_edit, name='settings_user_edit'),
    # Ajax requests
    #url(r'^settings/db/reset/$', settings_db_reset, name='settings_db_reset'),
    #url(r'^settings/db/scan/$', settings_db_scan, name='settings_db_scan'),
    #url(r'^settings/db/scan/info/$',settings_db_scan_info, name='settings_db_scan_info'),
    
    # Index view
    url(r'^$', index, name='index'),
    # Ajax requests for index view 
#    url(r'^collection/$', index_collection, name='index_collection'),
#    url(r'^search/artist/letter/(?P<artist>.*)/$', search_artist_letter, name='search_artist_letter'),
#    url(r'^search/all/(?P<search>.*)/$', search, name='search'),
#    url(r'^search/advanced/$', search_advanced, name='search_advanced'),
#    url(r'^search/autocomplete/(?P<row>.*)/$', search_autocomplete, name='search_autocomplete'),
#    url(r'^song/meta/(?P<id>.*)/$', song_meta, name='song_meta'),
    url(r'^song/download/(?P<id>.*)/$', song_download, name='song_download'),
#    url(r'^song/scrobble/(?P<id>.*)/$', song_scrobble, name='song_scrobble'),
#    url(r'^song/cover/(?P<id>.*)/$', song_cover, name='song_cover'),
    
    # Ajax playlist requests
#    url(r'^playlist/save/(?P<playlistName>.*)/$', playlist_save, name='playlist_save'),
#    url(r'^playlist/exists/(?P<playlistName>.*)/$', playlist_exists, name='playlist_exists'),
#    url(r'^playlist/name/(?P<playlistId>.*)/$', playlist_name, name='playlist_name'),
#    url(r'^playlist/open/(?P<playlistId>.*)/$', playlist_open, name='playlist_open'),
#    url(r'^playlist/delete/(?P<playlistId>.*)/$', playlist_delete, name='playlist_delete'),
#    url(r'^playlist/rename/(?P<oldName>.*)/(?P<newName>.*)/$', playlist_rename, name='playlist_rename'),
#    url(r'^playlist/list/$', playlist_list, name='playlist_list'),
    
    # Ampache XML API
    url(r'^server/xml.server.php$', xml_api, name='xml_api'),
    
    # Other sites
    url(r'^profile/$', profile, name='profile'),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', 
        {
            'template': 'about.html', 
            'extra_context': { 'version': django_settings.LAUDIO_VERSION }
        }
        , name='about'),
    url(r'^chat/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'chat.html'}, name='chat'),
    url(r'^login/', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'template_name': 'logout.html'}, name='logout'),

)
