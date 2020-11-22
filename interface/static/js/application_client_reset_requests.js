// ================ RESETS ================

function reset_face_comparison() {

    if (!start_capturing_and_requesting) {
        // reset values
        $.ajax({
            type: "GET",
            enctype: "multipart/form-data",
            url: API_BASE_URL + "reset_face_comparison",
            processData: false,
            contentType: false,
            cache: false,
            timeout: REQUESTS_TIMEOUT,
            complete: function (xhr) {
                let status = xhr.status;
                let response = xhr.responseJSON;
                let error_message;
                switch (status) {
                    case 200:
                        if (response["similitude_value"] === null &&
                            response["similitude_value_accumulative"] === null &&
                            response["similitude_value_best"] === null) {
                            $('#input_result_comp').attr('value', '%')
                            $('#input_result_comp_accumulative').attr('value', '%')
                            $('#input_result_comp_best').attr('value', '%')
                        }
                        break;
                    default:
                        break;
                }
            }
        });
    }
}

function reset_face_comparison_db() {

    // reset values
    $.ajax({
        type: "GET",
        enctype: "multipart/form-data",
        url: API_BASE_URL + "reset_face_comparison_db",
        processData: false,
        contentType: false,
        cache: false,
        timeout: REQUESTS_TIMEOUT,
        complete: function (xhr) {
            let status = xhr.status;
            let response = xhr.responseJSON;
            let error_message;
            switch (status) {
                case 200:
                    $('#input_identified_person_name').attr('value', "");
                    $('#input_accuracy').attr('value', "");
                    $("#p_status_comparison_db").text('Stopped and not running...');
                    $("#btn_acquire_frame").prop('disabled', false);
                    break;
                default:
                    break
            }
        }
    });
}

function reset_check_life() {

    // reset values
    $.ajax({
        type: "GET",
        enctype: "multipart/form-data",
        url: API_BASE_URL + "reset_check_life",
        processData: false,
        contentType: false,
        cache: false,
        timeout: REQUESTS_TIMEOUT,
        complete: function (xhr) {
            let status = xhr.status;
            let response = xhr.responseJSON;
            let error_message;
            switch (status) {
                case 200:
                    $("#p_status_comparison_db").text('Move the head to the...');
                    $("#svg_nopass_move_left").show();
                    $("#svg_pass_move_left").hide();
                    $("#svg_nopass_move_right").show();
                    $("#svg_pass_move_right").hide();
                    $("#svg_nopass_move_top").show();
                    $("#svg_pass_move_top").hide();
                    $("#svg_nopass_move_bot").show();
                    $("#svg_pass_move_bot").hide();
                    $("#btn_move_left").prop('disabled', false);
                    $("#btn_move_right").prop('disabled', false);
                    $("#btn_move_top").prop('disabled', false);
                    $("#btn_move_bot").prop('disabled', false);
                    break;
                default:
                    break
            }
        }
    });
}