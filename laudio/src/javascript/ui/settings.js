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

$(document).ready(function() { 

    /** 
     * This function resets the db when you click on it
     */
    $("#resetcoll").click(function() {
        // if popup is visible do nothing
        if( $("#popup").css("display") === "block" || 
            $(".small_loading").css("display") === "block" ){
            return;
        }

        // first we unbind any previously attached events
        $("#site").unbind("click");
        $("#deleteinfo").fadeIn("slow");
        
        // execute the ajax query which deletes the db
        $("#popup").load("{% url player:settings_db_reset %}", function (){ 
            $("#deleteinfo").fadeOut("slow", function() {
                $("#popup").slideDown("slow");
            });
            
            // add a fine animation to fade out the popup
            $("#site").bind("click", function() {
                $("#popup").slideUp("slow");
            });

        });     
          
    });
    

    /**
     * When you click on scan Collection this function gets executed
     * and starts a collection scan
     */
    $("#scancoll").click(function() {
        // if popup is visible do nothing
        if( $("#popup").css("display") === "block" || 
            $(".small_loading").css("display") === "block" ){
            return;
        }
        // first we unbind any previously attached events
        $("#site").unbind("click");
        $("#scaninfo").fadeIn("slow");
        
        // delete previous values
        clear_loaded();
        
        // wait 2 secs then set db querying
        timeout = setTimeout("query_start()",2000);
        
        // execute the ajax query which scans the collection
        $("#popup").load("{% url player:settings_db_scan %}", function (){ 
            $("#scaninfo").fadeOut("slow", function() {
                $("#popup").slideDown("slow");
                clearTimeout(timeout);
                clearInterval( db("timer", false) );
            });
            
            
            // add a fine animation to fade out the popup
            $("#site").bind("click", function() {
                $("#popup").slideUp("slow");
            });
            
        });
        
          
   
    });

});


var settings = {

    config : {
        scanUpdInterval : 5000,
        scannedTotal : "#total",
        scannedScanned : "#scanned",
        progressbar : $(".percentage canvas")[0]

    },
    

   progress_query_init : function(){
        db("timer", setInterval( settings._update_percentage(), 
            settings.config.scanUpdInterval ) );    
   },

    /**
     * Updates the progressbar by the queried value
     * Is being started by scan_start
     */
    _update_percentage : function(){
        $.getJSON("{% url player:settings_db_scan_info %}", function(json){
            $(settings.config.scannedScanned).html(json.scanned + "/");
            $(settings.config.scannedTotal).html(json.total);
            if(json.scanned !== 0){
                var percent = json.scanned / json.total;
                var width = Math.floor(percent * 300);
                var ctx = settings.config.progressbar.getContext("2d");
                ctx.clearRect(0,0, 300 ,24);
                // fill loaded bar
                ctx.fillStyle = "#333";
                ctx.fillRect(0,0, width ,24);
            }
        }); 
    },

    
    /**
     * Claers the progress bar
     */
    _clear_loaded : function(){
        $(settings.config.scannedScanned).html(0);
        $(settings.config.scannedTotal).html("");
        var ctx = settings.config.progressbar.getContext("2d");
        ctx.clearRect(0,0, 300 ,24);
    }

}
