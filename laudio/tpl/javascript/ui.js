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

var player, searching;
var $last_selected;
var shift_key = false;
var ctrl_key = false;
    
$(document).ready(function () {

    player = new Player(soundManager);
    searcher = new Search();
    $last_selected = player.id;
    
    // check config stuff
    {% if user.is_authenticated %}
    
        {% if user.get_profile.showLib %}
            searcher.simple('');
        {% endif %}
        
        {% if user.get_profile.hidePlaylist %}
            $('#playlist').css('display', 'none');
            $('#playlist_header').css('display', 'none');
        {% endif %}
        
        {% if user.get_profile.hideSidebar %}
            $('#sidebar').css('display', 'none');
            $('#sidebar_header').css('display', 'none');
        {% endif %}
        
    {% else %}
        {% if config.collectionStartup %}
            searcher.simple('');
        {% endif %}
    {% endif %}
    
    /***************************************************************************
     * navigation links
     **************************************************************************/
    $('#browser_link').click(function () {
        $('#browser').toggle('slide');
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


    /***************************************************************************
     * controls
     **************************************************************************/

    // progress bar
    $('#progress').slider({
        range: 'min',
        min: 0,
        max: 100
    });
    $('#progress').bind('slidestop', function (event, ui) {
        player.set_position($('#progress').slider('value'));
    });


    // volume bar
    $('#volume').slider({
        range: 'min',
        min: 0,
        max: 100,
        orientation: 'vertical'
    });
    $('#volume').slider('value', 100);
    $('#volume').bind('slide', function (event, ui) {
        player.set_volume($('#volume').slider('value'));
    });
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


    /**
     * Search
     */
    var timer;
    $('#search input').keyup(function(e) {
        if($(this).attr('value').length >= 2){
            clearTimeout( timer );
            var value = $(this).val();
            timer = setTimeout(function(){
                searcher.simple(value);
            }, 500);
        }
    });

    $('#browser #letter_browser td').click(function(){
        if($(this).attr('id') === 'load_all_songs'){
            searcher.simple('');
        } else {
            searcher.artist_letters($(this).html());
        }
        $('#browser').toggle('slide');
        $('#browser_link').toggleClass('active');
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
     * Tablesorting
     */
    $('#songlist table').tablesorter();
    $('.collNr').click( function() {
        activate_tablesorter(this, [[0,0],[2,0], [3,0], [4,0]], [[0,1], [2,0], [3,0], [4,0]] );
        return false;
    });
    $('.collTitle').click( function() {
        activate_tablesorter(this, [[1,0],[2,0], [3,0], [4,0]], [[1,1],[2,0], [3,0], [4,0]]);
        return false;
    });
    $('.collArtist').click( function() {
        activate_tablesorter(this, [[2,0], [3,0], [0,0]], [[2,1], [3,0], [0,0]]);
        return false;
    });
    $('.collAlbum').click( function() {
        activate_tablesorter(this, [[3,0], [2,0], [0,0]], [[3,1], [2,0], [0,0]]);
        return false;
    });
    $('.collGenre').click( function() {
        activate_tablesorter(this, [[4,0], [2,0], [3,0], [0,0]], [[4,1], [2,0], [3,0], [0,0]]);
        return false;
    });  


    // selecting lines
    $('#playlist tbody tr').click(function () {
        select_lines(this);
    });

});


/**
 * Plays the song of the row
 *
 * @param row: The dom element which we have clicked
 */
function play_row(row){
    player.play(row);
}


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
        $select_from.nextUntil('#' + $select_to.attr('id') + ' + *').addClass('selected');

    } else {
        $(row).addClass('selected');
        $last_selected = $(row);
    }
}

/**
 * Colors all lines in the collection
 * @param id: The table element which should be updated
 */
function update_line_colors(id){
    $(id + ' tbody tr').each(function(index) {
        if(index % 2){
            $(this).removeClass('line1');
            $(this).removeClass('line2');
            $(this).addClass('line2');
        } else {
            $(this).removeClass('line1');
            $(this).removeClass('line2');
            $(this).addClass('line1');
        }       
    });
}


/**
 * Runs a tablesort on the songlist
 * 
 * @param header_link: The link which was clicked on
 * @param sorting: The sorting for the songlist
 */
function activate_tablesorter (header_link, sorting_up, sorting_down) {
    var sorting;
    if($('#songlist table tbody tr').length > 1){
        if($(header_link).hasClass('sortup')){
            sorting = sorting_up;
            $('#songlist_header th').removeClass('sortup');
            $('#songlist_header th').removeClass('sortdown');
            $(header_link).addClass('sortdown');
        } else {
            $('#songlist_header th').removeClass('sortup');
            $('#songlist_header th').removeClass('sortdown');
            sorting = sorting_down;
            $(header_link).addClass('sortup');
        }
        $('#songlist table').trigger('sorton', [sorting]);
        update_line_colors('songlist table');
    }
}

/**
 * Filters categories by the row clicked on
 */
function filter_lines(row){
    $(row).siblings().removeClass('active');
    $(row).addClass('active');
    // dont load anything if he clicked on an empty field
    if($(row).html() === ''){
        return;
    }
    
    // start query for other fields
    var browser_id = $(row).parent().parent().parent().attr('id');
    if(browser_id === 'artist_browser'){
        searcher.advanced('', $(row).html(),  '', '');
    } else if(browser_id === 'album_browser'){
        searcher.advanced('', '',  $(row).html(), '');
    } else if(browser_id === 'genre_browser'){
        searcher.advanced('', '', '', $(row).html());
    }
    $('#browser').slideUp();
    $('#browser_link').toggleClass('active');
}

