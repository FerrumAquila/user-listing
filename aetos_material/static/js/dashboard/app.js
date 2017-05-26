jQuery.ajaxSetup({async:false});
$(document).ready(function() {

    var versions = [1, 2];

    $('#services-dashboard').children('.card-body').children('.container').html($('#services-dashboard').children('.card-body').children('.container').children('.dashboard-container').html())
    $('#apis-dashboard').children('.card-body').children('.container').html($('#apis-dashboard').children('.card-body').children('.container').children('.dashboard-container').html())

    $('body').on('click', '.service-delete', function(){
        delete_service($(this));
    });

    $('body').on('click', '.api-delete', function(){
        delete_api($(this));
    });

    $('body').on('click', '.dashboard-button', function(){
        var dashboard_li = $(this);
        switch_dashboard(dashboard_li);
    });

});