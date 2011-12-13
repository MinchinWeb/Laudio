/**
 * Laudio - A webbased musicplayer
 *
 * Copyright (C) 2010 Bernhard Posselt, bernhard.posselt@gmx.at
 *
 * Laudio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * Laudio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */


$(document).ready(function () {
    "use strict";

    var player,
        shift_key,
        ctrl_key,
        $last_selected;

    player = new Player();
    shift_key = false;
    ctrl_key = false;
    /***************************************************************************
     * navigation links
     **************************************************************************/
    $('#browser_link').click(function () {
        $('#browser').slideToggle();
        $(this).toggleClass('active');
    });

    $('#playlist_link').click(function () {
        $(this).toggleClass('active');
        $('#playlist').toggle('slide');
        $('#playlist_header').toggle('slide');
    });

    $('#sidebar_link').click(function () {
        $(this).toggleClass('active');
        $('#sidebar').toggle('slide');
        $('#sidebar_header').toggle('slide');
    });

    $('#profile_link').click(function () {
        $(this).toggleClass('active');
        $('#profile').slideToggle();
    });

    $('#settings_link').click(function () {
        $(this).toggleClass('active');
        $('#settings').slideToggle();
    });


    /***************************************************************************
     * controls
     **************************************************************************/

    // progress bar
    $('#progress').slider();
    $('#progress').slider('option', 'min', 0);
    $('#progress').slider('option', 'max', 100);
    $('#progress').bind('slidestop', function (event, ui) {
        player.set_position($('#progress').slider('value'));
    });


    // volume bar
    $('#volume').slider();
    $('#volume').slider('option', 'orientation', 'vertical');
    $('#volume').slider('option', 'min', 0);
    $('#volume').slider('option', 'max', 100);
    $('#volume').slider('value', 100);
    $('#volume').bind('slidechange', function (event, ui) {
        player.set_volume($('#volume').slider('value'));
    });
    $('#mute').hover(function () {
        $('#volume_container').css('display', 'block');
    }, function () {
        $('#volume_container').css('display', 'none');
    });
    $('#volume_container').hover(function () {
        $('#volume_container').css('display', 'block');
    }, function () {
        $('#volume_container').css('display', 'none');
    });


    // controls
    $('#controls .control #play_icon').click(function () {
        player.toggle_play_pause();
    });

    $('#controls .control .previous').click(function () {
        player.play_previous();
    });

    $('#controls .control .next').click(function () {
        player.play_next();
    });

    $('#controls .control #mute_icon').click(function () {
        player.toggle_mute();
    });

    $('#controls .control .jumpto').click(function () {
        document.location.hash = player.current_row_id();
    });

    $('#controls .control #shuffle_icon').click(function () {
        player.toggle_shuffle();
    });

    $('#controls .control #repeat_icon').click(function () {
        player.toggle_repeat();
    });


    /***************************************************************************
     * Playlist and Content
     **************************************************************************/
    // check for shift key pressed
    $(window).keydown(function (e) {
        if (e.which === 16) {
            shift_key = true;
            return false;
        }
    });
    $(window).keyup(function (e) {
        if (e.which === 16) {
            shift_key = false;
            return false;
        }
    });

    // check for ctrl key pressed
    $(window).keydown(function (e) {
        if (e.which === 17) {
            ctrl_key = true;
            return false;
        }
    });
    $(window).keyup(function (e) {
        if (e.which === 17) {
            ctrl_key = false;
            return false;
        }
    });


    /**
     * Function for selecting lines
     *
     * @param row: The dom element which we have clicked
     */
    function select_lines(row) {
        if (!(shift_key || ctrl_key)) {
            $(row).siblings().removeClass('selected');
        }

        var $select_from,
            $select_to;
        // check for shift selection
        if (shift_key) {
            // check if we have to select backwards or forwards
            if ($last_selected.index() <= $(row).index()) {
                $select_from = $last_selected;
                $select_to = $(row);
            } else {
                $select_from = $(row);
                $select_to = $last_selected;
            }
            $select_from.nextUntil('#' + $select_to.attr('id') + " + *").addClass('selected');

        } else {
            $(row).addClass('selected');
            $last_selected = $(row);
        }
    }

    // selecting lines
    $('#playlist tbody tr').click(function () {
        select_lines(this);
    });


    /***************************************************************************
     * Developement
     **************************************************************************/
    //$('#browser').css('display', 'block');
});
