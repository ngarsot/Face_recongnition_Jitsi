// ================ Main Client configuration ================

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
