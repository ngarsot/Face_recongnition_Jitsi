function initJitsi() {
    var rand = Math.floor(Math.random() * 10000000) + 100000;

    const domain = "meet.jit.si";
    const options = {
        roomName: 'Room_' + rand.toString(),
        parentNode: document.querySelector("#div_iframe_jitsi"),
    };
    api_jitsi = new JitsiMeetExternalAPI(domain, options);

    // Screen height to make the div to be filling the full screen
    var height_window = $(window).height();
    $("#div_container_of_body_elements").height(height_window);
    $("#div_iframe_jitsi").height(height_window);

}

function init_jitsi_config() {
    $("#btn_init_jitsi").click(function () {
        $("#id_div_btn_start_jitsi").remove();
        $("#ul_navs_index").prop("hidden", false);
        $("#id_div_btn_start_comparing").prop("hidden", false);
        $("#id_div_btn_finish_comparing").prop("hidden", false);
        $("#id_div_btn_reset").prop("hidden", false);
        $("#id_div_results").prop("hidden", false);
        initJitsi()
    })

    $("#btn_start_comparing").click(function () {
        for (var b in window) {
            if (b === 'api_jitsi') {
                api_jitsi.isVideoAvailable().then(available => {
                    if (api_jitsi.getParticipantsInfo().length !== 0) {
                        start_capturing_and_requesting = true;
                        $("#p_status_comparison").text('Running...');
                        captureScreenShot('face_comparison');
                    }
                })
            }
        }
    })

    $("#btn_finish_comparing").click(function () {
        start_capturing_and_requesting = false;
        $("#p_status_comparison").text('Not running...');
    })

    $("#btn_reset_face_comparison").click(function () {
        reset_face_comparison();
    })

    $("#btn_acquire_frame").click(function () {
        for (var b in window) {
            if (b === 'api_jitsi') {
                api_jitsi.isVideoAvailable().then(available => {
                    if (api_jitsi.getParticipantsInfo().length !== 0) {
                        $("#id_div_results_comparison_db").prop("hidden", false);
                        $("#p_status_comparison_db").text('Identifying...');
                        $("#id_div_btn_reset_face_comp_db").prop("hidden", false);
                        $("#btn_acquire_frame").prop('disabled', true);
                        captureScreenShot('face_comparison_db');

                    }
                })
            }
        }
    })

    $("#btn_reset_face_comparison_db").click(function () {
        reset_face_comparison_db();
    })

    $("#btn_move_left").click(function () {
        for (var b in window) {
            if (b === 'api_jitsi') {
                api_jitsi.isVideoAvailable().then(available => {
                    if (api_jitsi.getParticipantsInfo().length !== 0) {
                        $("#svg_nopass_move_left").hide();
                        $("#p_info_check_life").text('Acquiring frames...');
                        $("#btn_move_left").prop('disabled', true);
                        $("#btn_move_right").prop('disabled', true);
                        $("#btn_move_top").prop('disabled', true);
                        $("#btn_move_bot").prop('disabled', true);
                        captureScreenShot('check_life_left');
                    }
                })
            }
        }
    })

    $("#btn_move_right").click(function () {
        for (var b in window) {
            if (b === 'api_jitsi') {
                api_jitsi.isVideoAvailable().then(available => {
                    if (api_jitsi.getParticipantsInfo().length !== 0) {
                        $("#svg_nopass_move_right").hide();
                        $("#p_info_check_life").text('Acquiring frames...');
                        $("#btn_move_left").prop('disabled', true);
                        $("#btn_move_right").prop('disabled', true);
                        $("#btn_move_top").prop('disabled', true);
                        $("#btn_move_bot").prop('disabled', true);
                        captureScreenShot('check_life_right');
                    }
                })
            }
        }
    })

    $("#btn_move_top").click(function () {
        for (var b in window) {
            if (b === 'api_jitsi') {
                api_jitsi.isVideoAvailable().then(available => {
                    if (api_jitsi.getParticipantsInfo().length !== 0) {
                        $("#svg_nopass_move_top").hide();
                        $("#p_info_check_life").text('Acquiring frames...');
                        $("#btn_move_left").prop('disabled', true);
                        $("#btn_move_right").prop('disabled', true);
                        $("#btn_move_top").prop('disabled', true);
                        $("#btn_move_bot").prop('disabled', true);
                        captureScreenShot('check_life_top');
                    }
                })
            }
        }
    })

    $("#btn_move_bot").click(function () {
        for (var b in window) {
            if (b === 'api_jitsi') {
                api_jitsi.isVideoAvailable().then(available => {
                    if (api_jitsi.getParticipantsInfo().length !== 0) {
                        $("#svg_nopass_move_bot").hide();
                        $("#p_info_check_life").text('Acquiring frames...');
                        $("#btn_move_left").prop('disabled', true);
                        $("#btn_move_right").prop('disabled', true);
                        $("#btn_move_top").prop('disabled', true);
                        $("#btn_move_bot").prop('disabled', true);
                        captureScreenShot('check_life_bot');
                    }
                })
            }
        }
    })

    $("#btn_reset_check_life").click(function () {
        reset_check_life();
    })

}

function captureScreenShot(which_application) {
    let screenShot = api_jitsi.captureLargeVideoScreenshot().then(dataURL => {
        let dataFrame = dataURL.dataURL
        if (which_application === 'face_comparison') {
            send_frame_face_comparison(dataFrame);
        } else if (which_application === 'face_comparison_db') {
            send_frame_face_comparison_db(dataFrame)
        } else if (which_application === 'check_life_left') {
            send_frame_check_life(dataFrame, 'check_life_left')
        } else if (which_application === 'check_life_right') {
            send_frame_check_life(dataFrame, 'check_life_right')
        } else if (which_application === 'check_life_top') {
            send_frame_check_life(dataFrame, 'check_life_top')
        } else if (which_application === 'check_life_bot') {
            send_frame_check_life(dataFrame, 'check_life_bot')
        }
    });
}

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