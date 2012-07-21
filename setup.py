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
	            'src/laudio', 
	                'src/laudio/src', 
	                    'src/laudio/src/song', 
	                        'src/laudio/src/song/codecs', 
	                    'src/laudio/src/inc', 
	                'src/laudio/player', 
	                    'src/laudio/player/views',
	                        'src/laudio/player/views/templatetags',
	],
	package_data = {
	    '' : [
            'src/laudio/locale/*',
                'src/laudio/locale/de/*',
                    'src/laudio/locale/de/LC_MESSAGES/*',
	        'src/laudio/static/*', 
	            'src/laudio/static/img/*', 
	            'src/laudio/static/style/*',
	                'src/laudio/static/style/lib/*',
	                    'src/laudio/static/style/lib/images/*',
	            'src/laudio/static/upload/*',
	                'src/laudio/static/upload/themes/*',
	                    'src/laudio/static/upload/themes/default/*',
                            'src/laudio/static/upload/themes/default/font/*',  
                            'src/laudio/static/upload/themes/default/img/*',
	            'src/laudio/static/js/*', 
                    'src/laudio/static/js/lib/*',
                        'src/laudio/static/js/lib/jquery/*',
                        'src/laudio/static/js/lib/soundmanager/*',
                        'src/laudio/static/js/lib/soundmanager/script/*',
                        'src/laudio/static/js/lib/soundmanager/src/*',
                        'src/laudio/static/js/lib/soundmanager/swf/*',
	        'src/laudio/tpl/*', 
	            'src/laudio/tpl/ajax/*',
	            'src/laudio/tpl/config/*',
	            'src/laudio/tpl/install/*',
	            'src/laudio/tpl/javascript/*',
	            'src/laudio/tpl/player/*',
	            'src/laudio/tpl/xml/*',
	        'src/laudio/wsgi/django.wsgi',
	    ]
	}
)

