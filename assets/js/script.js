$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$(document).ready(function() {

    $('.cnp-produce-add').on('click', function() {

        var id_item_size = $(this).data('item_size-id');
        var amount = $('#produce-amount-'+id_item_size).val();
        if (amount != '') {
            $.ajax({
                url: '/produce-add/' + id_item_size + '/' + amount + '/',
                type: 'post',
                success: function(data) {
                    if (data.success) {
                        location.reload();
                    } else {
                    }
                }
            });
        };
    });

    $('.cnp-produce-del').on('click', function() {

        var id_item_size = $(this).data('item_size-id');
        $.ajax({
            url: '/produce-del/' + id_item_size + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cnp-piece-rotate').on('click', function() {

        var piece_id = $(this).data('piece-id');
        $.ajax({
            url: '/piece_rotate/' + piece_id + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cnp-produce-result-nesting').on('click', function() {

        var roll_id = $('#id_roll').val();

        $.ajax({
            url: '/produce_result_nesting/' + roll_id + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
   });

    $('.cnp-produce-result-validate').on('click', function() {

        var roll_id = $('#id_roll').val();

        $.ajax({
            url: '/produce_result_validate/' + roll_id + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
   });


});



