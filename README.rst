===============================
 l-audio - An HTML5 audioplayer
===============================

.. image::  https://dl.dropbox.com/u/15205713/screenshot_v05_small.png

:Version: 0.6.0.0
:Keywords: python, jquery, django, web, html5, audio, player, javascript, last.fm, libre.fm, json, mp3, ogg, vorbis

l-audio is a webbased player which takes advantage of the HTML5 audio element to 
play its music. Its aim is to provide a better interface than its competitor
Ampache.

l-audio is based on the Python Framework Django and uses Apache as server.
Installed on the machine where your music collection resides, it can be accessed
in the whole network. By forwarding Port 80 on your router,
even your friends can listen to it over the Internet.

Get a live preview on http://laudio-player.org/

Dependencies
============
* python-lxml 
* python-django (1.3)
* python-mutagen 
* apache2 
* sqlite3 
* libapache2-mod-wsgi 
* python-pysqlite2 
* ttf-dejavu
* ffmpeg

Installing 
==========

Git
---
To get the unstable trunk fire up your console and change to the path where you
want the source to be downloaded. Then type in::

    $ git clone git@github.com:Raydiation/Laudio.git
    $ cd Laudio*
    $ sudo /bin/bash setup.sh


Translation
===========
To translate l-audio into your language, you must do the following. First
get your language code on http://www.gnu.org/software/gettext/manual/gettext.html#Language-Codes
This code will be referenced as $LGCODE in this documentation. Then go
into the main directory and run::

    $ django-admin.py makemessages -l $LGCODE -e js
    
To update the language files to the current status, run::

    $ django-admin.py makemessages -a

If you made all your changes, you need to compile the translation into a
format which can be read by gettext. To do this, simply run::

    $ django-admin.py compilemessages
    
If you've added a new language, you must change the LANGUAGE dictionairy
in the settings.py file by adding the corresponding language.

Finally update the setup.py in the top directory to include your directory.

Working on an existing translation
----------------------------------
Update the translations by running::

    $ django-admin.py makemessages -a

Then make your changes to the translation file in locale/$LGCODE/LC_MESSAGES/django.po
and compile the messages with this command when you're done::

    $ django-admin.py compilemessages

Example for adding polish language translation
----------------------------------------------
Go into the main directory and run::

    $ django-admin.py makemessages -l pl -e js
    $ django-admin.py makemessages -a
    
Edit the file in locale/pl/LC_MESSAGES/django.po then compile your messages::

    $ django-admin.py compilemessages


Now activate the translation in the settings.py. To do this change this::

    LANGUAGES = (
        ('de', _('German')),
        ('en', _('English')),
    )

to this::

    LANGUAGES = (
          ('de', _('German')),
          ('en', _('English')),
          ('pl', _('Polish')),
    )
    
Then update the setup.py and by adding this to package_data::

    'laudio/locale/pl/*',
        'laudio/locale/pl/LC_MESSAGES/*',
        

Security
========
To only allow access from apache to your music directory please change the 
/etc/laudio/apache/laudio.conf::
    
    <Directory />

to::
    
    <Directory /your/music/directory/>



FAQ
===

How can i use l-audio with lighttpd?
------------------------------------
TBD

How can i use l-audio with mysql?
---------------------------------
First of all, you need python-mysql, depending on your distro the package can
be named ``python-mysql`` or ``mysql-python``. Then you have to change the 
/usr/share/laudio/laudio/settings.py from::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': LAUDIO_SQLITE_PATH,    # Or path to database file if using sqlite3.
            #'USER': '',                      # Not used with sqlite3.
            #'PASSWORD': '',                  # Not used with sqlite3.
            #'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            #'PORT': '',                      # Set to empty string for default. Not used with sqlite3.  
        }
    }

to::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mysql_database',    # Or path to database file if using sqlite3.
            'USER': 'mysql_user',                      # Not used with sqlite3.
            'PASSWORD': 'mysql_password',                  # Not used with sqlite3.
            'HOST': 'mysql_host',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': 'mysql_port',                      # Set to empty string for default. Not used with sqlite3.  
        }
    }
    
Then you have to recreate the database::

    python /usr/share/laudio/laudio/manage.py syncdb --noinput
    
And restart your webserver::

    /etc/init.d/apache2 restart

The same procedure basically applies to other databases like oracle and postgresql.

Which Browsers does l-audio support?
-----------------------------------
Depends wether you want to use MP3 or OGG VORBIS

``MP3``: All, Flash required

``OGG``: Google Chrome, Chromium, Opera, Firefox


What filerights should my musicdirectory have?
----------------------------------------------
The music files should be chmoded 0755. Every folder above the files has
to have a+x, so Apache can traverse down into the directory


How can i change the URL under which l-audio is being run
--------------------------------------------------------
If you want to let l-audio run under a different URL then localhost/laudio, like
localhost/audio for instance, you can now easily adjust it.

Open the /etc/laudio/apache/laudio.conf and change the two lines to::

    Alias /audio/static/ /usr/share/laudio/laudio/static/
    WSGIScriptAlias /audio /usr/share/laudio/laudio/static/django.wsgi

Finally restart your Apache webserver.

    sudo /etc/init.d/apache2 restart



Getting Help
============

IRC
---

We reside on irc.freenode.net in channel ``#laudio``.

Messenger & Email
-----------------

If you dont reach me in IRC, i dont mind if you ask me via Messenger or Email:

email: bernhard.posselt@gmx.at

jabber: xray99@jabber.ccc.de

Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them
to our issue tracker at http://github.com/Raydiation/Laudio/issues

Contributing
============

To contribute send a mail to: bernhard.posselt@gmx.at or join the channel
on Freenode or just simply send me a pull request ;)

License
=======

This software is licensed under the ``GPLv3``. See the ``COPYING``
file in the top directory for the full license text.

