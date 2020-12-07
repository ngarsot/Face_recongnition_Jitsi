"""
    main.py
    ~~~~~~~~~

    This module implements the Face_recognition Jitsi server. To launch it, simply execute this file

"""

from os import path, listdir

from flask import Flask, request, render_template

from src.check_life import check_life as cl
from src.face_comparison import face_comparison as fi
from src.face_comparison import face_comparison_db as fi_db
from src.jitsi_app import jitsi_app
from src.jitsi_app.constants import *

# Flask object initialization and some configuration parameters
app = Flask(__name__,
            template_folder=TEMPLATES_FOLDER,
            static_folder=STATIC_FOLDER)
app.secret_key = 'jitsi_app_fr'
app.config["JSON_SORT_KEYS"] = True

# Globals objects
face_comparison = fi.FaceComparison()
face_comparison_db = fi_db.FaceComparisonDB()
face_check_life = cl.Checklife()
jitsi_application = jitsi_app.JitsiApp()


# ============ For all requests ============
@app.after_request
def add_header(r):
    """
    Add header to disable cache
    """

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


# ============ INDEX page request ============
@app.route('/')
@app.route('/index')
def jitsi_app():
    """
    The request that sends the index page. First request.
    """

    return render_template('jitsi.html')


# ============ MAIN requests ============
@app.route('/get_similitude', methods=['GET', 'POST'])
def get_similitude():
    """
    The request accepts a frame via POST in dataURL format. It parses it, and extracts two faces in order
    to compare them. The result is returned in a dict format.

    :return: returns a dict with the generated results (Log,
                                                        similitude_value,
                                                        similitude_value_accumulative,
                                                        similitude_value_best).
    """

    global face_comparison
    # Return content by default or in case of exception
    content = {'Log': 'Frame not processed correctly',
               'similitude_value': None,
               'similitude_value_accumulative': None,
               'similitude_value_best': None}
    try:
        if 'dataURL_frame' in request.form.keys():
            # Gets the dataURL and parse it
            data_url_frame = request.form['dataURL_frame']
            face_comparison.set_pixels_image_from_data_url(data_url_frame)
            # Extract features of the detected faces
            face_comparison.extract_face_128d_features_from_single_photo()
            if len(face_comparison.dni_person_encoding):
                # Compare the extracted features of both detected faces
                face_comparison.compare_encoded_faces()
                content = {'Log': 'Frame processed correctly',
                           'similitude_value': face_comparison.face_comparison_result,
                           'similitude_value_accumulative': face_comparison.face_comparison_accumulative_result,
                           'similitude_value_best': face_comparison.face_comparison_best_result}

        return content, HTTP_200_OK

    except Exception:
        return content, HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/get_similitude_from_db', methods=['GET', 'POST'])
def get_similitude_from_db():
    """
    The request accepts a frame via POST in dataURL format. It parses it, and extracts the face in order
    to compare with a DB. The result is returned in a dict format.

    :return: returns a dict with the generated results (Log,
                                                        person_identified_name,
                                                        accuracy).
    """

    global face_comparison_db
    # Return content by default or in case of exception
    content = {'Log': 'Search not processed correctly',
               'person_identified_name': None,
               'accuracy': None}
    try:
        if 'dataURL_frame' in request.form.keys():
            # Gets the dataURL and parse it
            data_url_frame = request.form['dataURL_frame']
            # Extract features of the frame detected face.
            face_comparison_db.encoding_person(data_url=data_url_frame)
            # Then, it iterate for all the DB photos and extracts and compares with the target one.
            '''
            # It is possible to have the set of photos in a dir and conduct the comaprison there. The name
            # of the photo file must be the name of the person inside the photo. If you want to use like this
            # uncomment this lines and comment the fowolling one (face_comparison_db.load_encoding_unknown_from_db()).
            DB_PHOTO_PATH_HARDCODED = 'src/test_files/test_data/db/'
            for photo in listdir(DB_PHOTO_PATH_HARDCODED):
                photo_path = path.join(DB_PHOTO_PATH_HARDCODED, photo)
                face_comparison_db.encoding_unknown(image_path=photo_path)
                face_comparison_db.compare_encodings()
            '''
            face_comparison_db.load_encoding_unknown_from_db(DB)

            content = {'Log': 'Search processed correctly',
                       'person_identified_name': face_comparison_db.person_possible_identified,
                       'accuracy': face_comparison_db.face_comp_best_result_pearson}
            face_comparison_db.reset()

        return content, HTTP_200_OK

    except Exception as e:
        print(str(e))
        return content, HTTP_205_RESET_CONTENT


@app.route('/store_frames_in_buffer', methods=['GET', 'POST'])
def store_frames_in_buffer():
    """
    The request accepts frames via POST in dataURL format.
    The frames are parsed and stored in the buffer until it is full.

    :return: returns a dict with the buffer status (Log, status_acquiring).
    """

    global face_check_life
    # Return content by default or in case of exception
    content = {'Log': 'Check life not processed correctly',
               'status_acquiring': True, }
    try:
        if not face_check_life.is_buffer_max_len():
            if 'dataURL_frame' in request.form.keys():
                # Parses the dataURL and stores it in the buffer
                data_url_frame = request.form['dataURL_frame']
                face_check_life.set_pixels_image_from_data_url(data_url_frame)
                content = {'Log': 'Still capturing',
                           'status_acquiring': True}
                if face_check_life.is_buffer_max_len():
                    content['status_acquiring'] = False
        return content, HTTP_200_OK

    except Exception as e:
        return content, HTTP_205_RESET_CONTENT


@app.route('/check_life_left', methods=['GET', 'POST'])
def check_life_left():
    """
    When the buffer is full, it generates the landmarks for all the photos stored there.
    Finally, it conducts the check life by checking a left head movement.

    :return: returns a dict with the test status (Log, status_check_life).
    """

    global face_check_life
    # Return content by default or in case of exception
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
        # Set landmarks when the buffer if full
        face_check_life.set_landmarks_for_all_faces_in_buffer()
        if face_check_life.check_if_left_move():
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': True}
        else:
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': False}
        face_check_life.reset()
        print(content, HTTP_200_OK)
        return content, HTTP_200_OK

    except Exception as e:
        return content, HTTP_205_RESET_CONTENT


@app.route('/check_life_right', methods=['GET', 'POST'])
def check_life_right():
    """
    When the buffer is full, it generates the landmarks for all the photos stored there.
    Finally, it conducts the check life by checking a right head movement.

    :return: returns a dict with the test status (Log, status_check_life).
    """

    global face_check_life
    # Return content by default or in case of exception
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
        # Set landmarks when the buffer if full
        face_check_life.set_landmarks_for_all_faces_in_buffer()
        if face_check_life.check_if_right_move():
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': True}
        else:
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': False}
        face_check_life.reset()
        return content, HTTP_200_OK

    except Exception as e:
        return content, HTTP_205_RESET_CONTENT


@app.route('/check_life_top', methods=['GET', 'POST'])
def check_life_top():
    """
    When the buffer is full, it generates the landmarks for all the photos stored there.
    Finally, it conducts the check life by checking a top head movement.

    :return: returns a dict with the test status (Log, status_check_life).
    """

    global face_check_life
    # Return content by default or in case of exception
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
        # Set landmarks when the buffer if full
        face_check_life.set_landmarks_for_all_faces_in_buffer()
        if face_check_life.check_if_top_move():
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': True}
        else:
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': False}
        face_check_life.reset()
        return content, HTTP_200_OK

    except Exception as e:
        return content, HTTP_205_RESET_CONTENT


@app.route('/check_life_bot', methods=['GET', 'POST'])
def check_life_bot():
    """
    When the buffer is full, it generates the landmarks for all the photos stored there.
    Finally, it conducts the check life by checking a bottom head movement.

    :return: returns a dict with the test status (Log, status_check_life).
    """

    global face_check_life
    # Return content by default or in case of exception
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
        # Set landmarks when the buffer if full
        face_check_life.set_landmarks_for_all_faces_in_buffer()
        if face_check_life.check_if_bot_move():
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': True}
        else:
            content = {'Log': 'Check life processed correctly',
                       'status_check_life': False}
        face_check_life.reset()
        return content, HTTP_200_OK

    except Exception as e:
        return content, HTTP_205_RESET_CONTENT


# ============ RESET requests ============
@app.route('/reset_face_comparison', methods=['GET'])
def reset_face_comparison():
    """
    It resets the FaceComparison class and resets the UI values.

    :return: returns a dict with the reset parameters (Log,
                                                        similitude_value,
                                                        similitude_value_accumulative,
                                                        similitude_value_best).
    """

    global face_comparison
    face_comparison.reset()
    content = {'Log': 'Reset correctly performed',
               'similitude_value': face_comparison.face_comparison_result,
               'similitude_value_accumulative': face_comparison.face_comparison_accumulative_result,
               'similitude_value_best': face_comparison.face_comparison_best_result}

    return content, HTTP_200_OK


@app.route('/reset_face_comparison_db', methods=['GET'])
def reset_face_comparison_db():
    """
    It resets the FaceComparisonDB.

    :return: returns a dict with the reset parameters (Log).
    """

    global face_comparison_db
    face_comparison_db.reset()
    content = {'Log': 'Reset correctly performed'}

    return content, HTTP_200_OK


@app.route('/reset_check_life', methods=['GET'])
def reset_check_life():
    """
    It resets the Checklife class.

    :return: returns a dict with the reset parameters (Log).
    """

    global face_check_life
    face_check_life.reset()
    content = {'Log': 'Reset correctly performed'}

    return content, HTTP_200_OK


if __name__ == '__main__':
    # Runs the flask object. The Server starts here!
    app.run(debug=True)
