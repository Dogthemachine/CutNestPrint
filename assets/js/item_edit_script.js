$(document).ready(function() {

    $('.cnp-item-size-del').on('click', function() {

        var id_size = $(this).data('size-id');
        var id_item = $(this).data('item-id');
        $.ajax({
            url: '/item-size-del/' + id_item + '/' + id_size + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
//                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cnp-piece-del').on('click', function() {

        var id_piece = $(this).data('piece-id');
        $.ajax({
            url: '/piece-del/' + id_piece + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                    location.reload();
                } else {
                }
            }
        });
    });

    $('.cnp-delete-item').on('click', function() {

        var id_item = $(this).data('item-id');

        $.ajax({
            url: '/delete_item/' + id_item + '/',
            type: 'post',
            success: function(data) {
                if (data.success) {
                window.location.replace(window.location.protocol.toString() + "//" + window.location.host.toString() + "/fashions/");
                } else {
                }
            }
        });
   });

});