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

jQuery(document).ready(function(){

    jQuery("#document-action-socialbookmark > a").click(function(event) {
        event.preventDefault();
        sb_delay_clear();
        jQuery("div.social_bookmarks").toggle();
    });
    jQuery("#document-action-socialbookmark > a").mouseover(function(event) {
        sb_delay_clear();
        jQuery("div.social_bookmarks").show();
    });
    jQuery("#document-action-socialbookmark > a").mouseout(function(event) {
        sb_delay_function(function() {
            jQuery("div.social_bookmarks").hide();
        });
    });
    jQuery("div.social_bookmarks").mouseover(function(event) {
        sb_delay_clear();
        jQuery("div.social_bookmarks").show();
    });
    jQuery("div.social_bookmarks").mouseout(function(event) {
        jQuery("div.social_bookmarks").hide();
    });
});
