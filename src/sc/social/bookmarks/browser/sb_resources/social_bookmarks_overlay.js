(function($) {

    var sb_timeout = 0;
    var sb_timeout_delay = 200;
    
    function sb_delay_function(fun) {
        sb_delay_clear();
        sb_timeout = window.setTimeout(fun, sb_timeout_delay);
    }
    function sb_delay_clear() {
        if (sb_timeout) {
            window.clearTimeout(sb_timeout);
        }
    }
    
    $(document).ready(function() {
        
        $("#document-action-socialbookmark > a").click(function(event) {
            event.preventDefault();
            sb_delay_clear();
            $("div.sc_social_bookmarks_overlay").toggle();
        });
        
        $("#document-action-socialbookmark > a").mouseover(function(event) {
            sb_delay_clear();
            $("div.sc_social_bookmarks_overlay").show();
        });
        
        $("#document-action-socialbookmark > a").mouseout(function(event) {
            sb_delay_function(function() {
                $("div.sc_social_bookmarks_overlay").hide();
            });
        });
        
        $("div.sc_social_bookmarks_overlay").mouseover(function(event) {
            sb_delay_clear();
            $("div.sc_social_bookmarks_overlay").show();
        });
        
        $("div.sc_social_bookmarks_overlay").mouseout(function(event) {
            $("div.sc_social_bookmarks_overlay").hide();
        });
        
    });

})(jQuery);