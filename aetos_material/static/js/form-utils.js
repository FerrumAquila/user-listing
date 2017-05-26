jQuery.ajaxSetup({async:false});
$(document).ready(function() {

    serialize_form = function(form_id, serialize_type){
        var html_form = $('#' + form_id);
        switch(serialize_type){
            case 'json':
                var form_array = html_form.serializeArray();
                var form_json = {};
                $.each(form_array, function(i){
                    key = form_array[i].name;
                    value = form_array[i].value;
                    if(form_json.hasOwnProperty(key)){
                        multiselect = form_json[key];
                        if(!(multiselect.constructor == Array)){
                            multiselect = [get_valid_form_value(key, value), multiselect];
                        }else{
                            multiselect.push(get_valid_form_value(key, value));
                        }
                        var cleaned_value = multiselect;
                    }else{
                        var cleaned_value = get_valid_form_value(key, value);
                    }
                    form_json[key] = cleaned_value;
                });
                return form_json
            case 'array':
                return html_form.serializeArray()
            case 'query_string':
                return html_form.serialize()
            default:
                return html_form.serialize()
        }
    };

    var add_parent_id = function(data, html_form){
        var parent_value = html_form.data('parent-id');
        if(parent_value){
            var parent_key = html_form.data('parent-key');
            data += ('&' + parent_key + '=' + parent_value);
            return data
        }
        return data
    };

    var get_valid_form_value = function(key, value){
        switch(key){
            // add special cases to be handled here
            default:
                var valid_form_value = value;
                break;
        }
        return valid_form_value
    };

    var handle_form_group_on_create_success = function(form_group, responseJSON){
        var input_div = form_group.children('.input-div');
        var input_name = input_div.children('.fg-line').children().attr('name')

        if(responseJSON[input_name]){
            form_group.addClass('has-success');
            form_group.removeClass('has-error');
            input_div.children('.help-block').html('Entry Successful!');
            input_div.children('.md-warning').hide();
            input_div.children('.md-check').show();
            if(input_name == 'id'){
                if(!input_div.children('.fg-line').children('input').val()){
                    input_div.children('.fg-line').children('input').val(responseJSON[input_name]);
                }
            }
        }
    };

    var handle_form_group_on_create_failure = function(form_group, errorJSON){
        var input_div = form_group.children('.input-div');
        var input_name = input_div.children('.fg-line').children().attr('name')

        form_group.removeClass('has-success');
        form_group.removeClass('has-error');
        input_div.children('.help-block').html('')
        input_div.children('.md-warning').hide();

        if(errorJSON[input_name]){
            form_group.addClass('has-error');
            input_div.children('.help-block').html(errorJSON[input_name][0]);
            input_div.children('.md-warning').show();
        }
    };

    form_action = function(form_id, action){
        var html_form = $('#' + form_id);
        var url = html_form.attr('action');
        var data = html_form.serialize()
        data = add_parent_id(data, html_form)
        if(serialize_form(form_id, 'json').id){
            switch(action){
                case 'create':
                    var action = 'update';
                    break;
                case 'remove':
                    var action = 'delete';
                    url = url.replace('update', 'delete')
                    break;
            }
        }else{
            switch(action){
                case 'update':
                    var action = 'create';
                    break;
                case 'remove':
                    var url = url.replace('create', 'delete')
                    break;
            }
        }
        var class_type = form_id.split('-')[0];
//        console.log('form id, action, url, data');
//        console.log(form_id);
//        console.log(action);
//        console.log(url)
//        console.log(data);
        switch(action){
            case 'create':
                $.post(url, data, function(response){
//                    dev_response = response;
//                    console.log(dev_response);
                    var responseJSON = response;
                    var form_groups = html_form.children('.row').children('.form-group')
                    $.each(form_groups, function(i){
                        var form_group = form_groups.eq(i);
                        handle_form_group_on_create_success(form_group, responseJSON);
                    });
                    html_form.attr('action', html_form.attr('action').replace('create', 'update') + responseJSON.id + '/');

                }).fail(function(error){
//                    dev_error = error;
//                    console.log(dev_error);
                    alert('error in ' + class_type + ' forms\nplease fix');
                    var errorJSON = JSON.parse(error.responseText);
                    var form_groups = html_form.children('.row').children('.form-group')
                    $.each(form_groups, function(i){
                        var form_group = form_groups.eq(i);
                        handle_form_group_on_create_failure(form_group, errorJSON);
                    });

                });
                break;
            case 'update':
                $.put(url, data, function(response){
//                    dev_response = response;
//                    console.log(dev_response);
                    var responseJSON = response;
                    var form_groups = html_form.children('.row').children('.form-group')
                    $.each(form_groups, function(i){
                        var form_group = form_groups.eq(i);
                        handle_form_group_on_create_success(form_group, responseJSON);
                    });

                }).fail(function(error){
//                    dev_error = error;
//                    console.log(dev_error);
                    alert('error in ' + class_type + ' forms\nplease fix');
                    var errorJSON = JSON.parse(error.responseText);
//                    console.log(html_form.attr('id'))
                    var form_groups = html_form.children('.row').children('.form-group')
                    $.each(form_groups, function(i){
                        var form_group = form_groups.eq(i);
                        handle_form_group_on_create_failure(form_group, errorJSON);
                    });

                });
                break;
            case 'delete':
                $.delete(url, data, function(response){
//                    dev_response = response;
//                    console.log(dev_response);
                }).fail(function(error){
//                    dev_error = error;
//                    console.log(dev_error);
                });
            case 'remove':
                service_api_card = html_form.parent().parent().parent()
                service_api_card.remove()
                alert('removing card ' + service_api_card.attr('id'))
                break;
        }
    };

});