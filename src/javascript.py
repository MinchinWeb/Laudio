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
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

from django.template import Context, Template
from django.conf import settings

import os

class JavaScript(object):
    """This class is for enabling django template vars and template syntax
    in javascript files and manipulating the js for different views"""
    
    def __init__(self, view):
        """First we set the functions and files we have to include for
        the view we serve
        
        Keyword arguments:
        view -- can be: "library", "settings" or "playlist"; sets javascript
                according to those views
        
        """
        self.view = view
        
        files = ()
        """Depending on the view, different js files are being included. 
        We specify the ones we want to load with a files tuple, path 
        starting from src/javascript/"""
        if self.view == "library":
            files = ("inc/includes.js", "ui/collection.js", "ui/controls.js",
                     "ui/tablesorting.js", "ui/nav.js", "player/player.js")
                     
        elif self.view == "settings":
            files = ("ui/settings.js",)
            
        elif self.view == "playlist":
            files = ()
            
        else:
            files = ()
        
        content = ""
        # loop over files and build the content
        for f in files:
            # get the javascript from the file
            fh = os.path.join(settings.INSTALL_DIR, "src/javascript/%s" % f )
            file = open(fh, 'r')
            content += file.read()
            file.close()
        
        
        # create template and parse context
        tpl = Template(content)
        context = Context( {} )
        self.javascript = tpl.render(context)


    def __str__(self):
        return self.javascript