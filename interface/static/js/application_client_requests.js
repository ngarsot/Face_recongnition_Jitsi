// ================ AJAX requests ================

function send_frame_face_comparison(data_URL_frame) {

    // Build data to be sent
    let form_data = new FormData();
    form_data.append("dataURL_frame", data_URL_frame);

    // Send frame
    $.ajax({
        type: "POST",
        enctype: "multipart/form-data",
        url: API_BASE_URL + "get_similitude",
        data: form_data,
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
                    if (response["similitude_value"] !== null) {
                        $('#input_result_comp').attr('value', response["similitude_value"] + '%')
                        $('#input_result_comp_accumulative').attr('value', response["similitude_value_accumulative"] + '%')
                        $('#input_result_comp_best').attr('value', response["similitude_value_best"] + '%')
                    } else {
                        $('#input_result_comp').attr('value', '%')
                    }
                    if (start_capturing_and_requesting) {
                        captureScreenShot('face_comparison')
                    }
                    break;
                default:
                    reset_face_comparison()
                    start_capturing_and_requesting = false;
                    $("#p_status_comparison").text('Not running...');
            }
        }
    });
}

function send_frame_face_comparison_db(data_URL_frame) {

    // Build data to be sent
    let form_data = new FormData();
    form_data.append("dataURL_frame", data_URL_frame);

    // Send frame
    $.ajax({
        type: "POST",
        enctype: "multipart/form-data",
        url: API_BASE_URL + "get_similitude_from_db",
        data: form_data,
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
                    $("#p_status_comparison_db").text('Not running...');
                    $("#btn_acquire_frame").prop('disabled', false);
                    if (response["accuracy"] !== null || response["accuracy"] !== '0') {
                        $('#input_identified_person_name').attr('value', response["person_identified_name"])
                        $('#input_accuracy').attr('value', response["accuracy"] + '%')
                    } else {
                        $('#input_identified_person_name').attr('value', "Unknown")
                        $('#input_accuracy').attr('value', 'Undefined')
                    }
                    break;
                default:
                    reset_face_comparison_db()
                    $("#p_status_comparison_db").text('Stopped and not running...');
                    $("#btn_acquire_frame").prop('disabled', false);
            }
        }
    });
}

function send_frame_check_life(data_URL_frame, which_check_life) {
    // Build data to be sent
    let form_data = new FormData();
    form_data.append("dataURL_frame", data_URL_frame);
    let url_request = which_check_life;

    // Send frame
    $.ajax({
        type: "POST",
        enctype: "multipart/form-data",
        url: API_BASE_URL + 'store_frames_in_buffer',
        data: form_data,
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
                    if (response["status_acquiring"]) {
                        captureScreenShot(url_request)
                    } else {
                        $("#p_info_check_life").text('Testing head movement...');
                        request_for_check_life(url_request)
                    }
                    break
                default:
                    reset_check_life()
                    break
            }
        }
    });
}

function request_for_check_life(which_check_life) {
    let url_request = which_check_life;

    // Send frame
    $.ajax({
        type: "POST",
        enctype: "multipart/form-data",
        url: API_BASE_URL + url_request,
        processData: false,
        contentType: false,
        cache: false,
        timeout: REQUESTS_TIMEOUT,
        complete: function (xhr) {
            let status = xhr.status;
            let response = xhr.responseJSON;
            switch (status) {
                case 200:
                    if (response["status_check_life"] === true) {
                        if (url_request === 'check_life_left') {
                            $("#svg_nopass_move_left").hide();
                            $("#svg_pass_move_left").show();
                        } else if (url_request === 'check_life_right') {
                            $("#svg_nopass_move_right").hide();
                            $("#svg_pass_move_right").show();
                        } else if (url_request === 'check_life_top') {
                            $("#svg_nopass_move_top").hide();
                            $("#svg_pass_move_top").show();
                        } else if (url_request === 'check_life_bot') {
                            $("#svg_nopass_move_bot").hide();
                            $("#svg_pass_move_bot").show();
                        }
                    } else {
                        if (url_request === 'check_life_left') {
                            $("#svg_pass_move_left").hide();
                            $("#svg_nopass_move_left").show();
                        } else if (url_request === 'check_life_right') {
                            $("#svg_pass_move_right").hide();
                            $("#svg_nopass_move_right").show();
                        } else if (url_request === 'check_life_top') {
                            $("#svg_pass_move_top").hide();
                            $("#svg_nopass_move_top").show();
                        } else if (url_request === 'check_life_bot') {
                            $("#svg_pass_move_bot").hide();
                            $("#svg_nopass_move_bot").show();
                        }
                    }
                    $("#p_status_comparison_db").text('Move the head to the...');
                    $("#btn_move_left").prop('disabled', false);
                    $("#btn_move_right").prop('disabled', false);
                    $("#btn_move_top").prop('disabled', false);
                    $("#btn_move_bot").prop('disabled', false);
                    break
                default:
                    reset_check_life()
                    break
            }
        }
    });
}
