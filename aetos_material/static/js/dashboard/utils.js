$(document).ready(function() {
    delete_service = function(service_row_btn){
        var service_id = service_row_btn.data('service-id');
        var url = service_row_btn.data('drf-url');

        $.delete(url, {}, function(response){
//            dev_response = response;
//            console.log(dev_response);
            service_row_btn.parent('td').parent('tr').remove();
        }).fail(function(error){
//            dev_error = error;
//            console.log(dev_error);
            alert('Error while deleting Page-' + page_id + ': "' + error.statusText + '"');
        });
    };

    delete_api = function(api_row_btn){
        var api_id = api_row_btn.data('api-id');
        var url = api_row_btn.data('drf-url');

        $.delete(url, {}, function(response){
//            dev_response = response;
//            console.log(dev_response);
            api_row_btn.parent('td').parent('tr').remove();
        }).fail(function(error){
//            dev_error = error;
//            console.log(dev_error);
            alert('Error while deleting Page-' + page_id + ': "' + error.statusText + '"');
        });
    };

    switch_dashboard = function(dashboard_li){
        var dashboard_id = dashboard_li.data('dashboard-id');

        $('.dashboard-button').removeClass('active')
        dashboard_li.toggleClass('active');

        $('.dashboard').hide();
        $('#' + dashboard_id).show();
    };

});