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

from distutils.core import setup

setup(
    name = 'laudio',
	version = '0.6.0.0',
	description = 'l-audio Music Player',
	author = 'Bernhard Posselt',
	author_email = 'bernhard.posselt@gmx.at',
	url = 'https://github.com/Raydiation/Laudio',
	packages = [
	            'laudio', 
	                'laudio/src', 
	                    'laudio/src/song', 
	                        'laudio/src/song/codecs', 
	                    'laudio/src/inc', 
	                'laudio/player', 
	                    'laudio/player/views',
	],
	package_data = {
	    '' : [
	        'laudio/static/*', 
	            'laudio/static/img/*', 
	            'laudio/static/style/*',
	                'laudio/static/style/lib/*',
	                    'laudio/static/style/lib/images/*',
	            'laudio/static/upload/*',
	                'laudio/static/upload/themes/*',
	                    'laudio/static/upload/themes/default/*',
                            'laudio/static/upload/themes/default/font/*',  
                            'laudio/static/upload/themes/default/img/*',                            
	            'laudio/static/js/*', 
                    'laudio/static/js/lib/*',
                        'laudio/static/js/lib/jquery/*',
                        'laudio/static/js/lib/soundmanager/*',
                        'laudio/static/js/lib/soundmanager/script/*',
                        'laudio/static/js/lib/soundmanager/src/*',
                        'laudio/static/js/lib/soundmanager/swf/*',
	        'laudio/tpl/*', 
	            'laudio/tpl/ajax/*',
	            'laudio/tpl/install/*',
	            'laudio/tpl/javascript/*',
	            'laudio/tpl/player/*',
	            'laudio/tpl/xml/*',
	        'laudio/wsgi/django.wsgi',
	    ]
	}
)

