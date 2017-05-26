$(document).ready(function () {
    $("#signInform").submit(function () {
        $.post('/login/', $(this).serialize(), function (response) {
            /* do something with returned data from server*/
            console.log(response);

            if (response.success == true) {
                window.location.href = "/dashboard/";
            } else {
                alert(response.error);
            }
        });
        return false;
        /* prevent browser submitting form*/
    });
});