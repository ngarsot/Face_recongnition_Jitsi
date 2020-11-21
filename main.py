from os import path, listdir

from flask import Flask, request, render_template

from src.check_life import check_life as cl
from src.face_comparison import face_comparison as fi
from src.face_comparison import face_comparison_db as fi_db
from src.jitsi_app import jitsi_app
from src.jitsi_app.constants import *

app = Flask(__name__,
            template_folder=TEMPLATES_FOLDER,
            static_folder=STATIC_FOLDER)
app.secret_key = 'jitsi_app_fr'
app.config["JSON_SORT_KEYS"] = True

face_comparison = fi.FaceComparison()
face_comparison_db = fi_db.FaceComparisonDB()
face_check_life = cl.Checklife()

jitsi_application = jitsi_app.JitsiApp()


# Disable cache
@app.after_request
def add_header(r):
    """ Add header to disable cache """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


@app.route('/')
def jitsi_app():
    return render_template('jitsi.html')


@app.route('/get_similitude', methods=['GET', 'POST'])
def get_similitude():
    global face_comparison
    content = {'Log': 'Frame not processed correctly',
               'similitude_value': None,
               'similitude_value_accumulative': None,
               'similitude_value_best': None}
    try:
        if 'dataURL_frame' in request.form.keys():
            data_url_frame = request.form['dataURL_frame']
            face_comparison.set_pixels_image_from_data_url(data_url_frame)
            # if face_comparison.detect_faces():
            #     face_comparison.extract_face_128d_features()
            #     face_comparison.compare_encoded_faces(from_single_photo=False)
            face_comparison.extract_face_128d_features_from_single_photo()
            if len(face_comparison.dni_person_encoding):
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
    global face_comparison_db
    content = {'Log': 'Search not processed correctly',
               'person_identified_name': None,
               'accuracy': None}
    try:
        if 'dataURL_frame' in request.form.keys():
            data_url_frame = request.form['dataURL_frame']
            DB_PHOTO_PATH_HARDCODED = 'src/test_files/test_data/db/'  # TODO change this with a real database and refactor the code
            face_comparison_db.encoding_person(data_url=data_url_frame)
            for photo in listdir(DB_PHOTO_PATH_HARDCODED):
                photo_path = path.join(DB_PHOTO_PATH_HARDCODED, photo)
                face_comparison_db.encoding_unknown(image_path=photo_path)
                face_comparison_db.compare_encodings()
            content = {'Log': 'Search processed correctly',
                       'person_identified_name': face_comparison_db.person_possible_identified,
                       'accuracy': face_comparison_db.face_comparison_best_result}
            face_comparison_db.reset()

        return content, HTTP_200_OK

    except Exception:
        return content, HTTP_205_RESET_CONTENT


@app.route('/store_frames_in_buffer', methods=['GET', 'POST'])
def store_frames_in_buffer():
    global face_check_life
    content = {'Log': 'Check life not processed correctly',
               'status_acquiring': True, }
    try:
        if not face_check_life.is_buffer_max_len():
            if 'dataURL_frame' in request.form.keys():
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
    global face_check_life
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
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
    global face_check_life
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
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
    global face_check_life
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
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
    global face_check_life
    content = {'Log': 'Check life not processed correctly',
               'status_check_life': False}
    try:
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


# ============ RESET # ============
@app.route('/reset_face_comparison', methods=['GET'])
def reset_face_comparison():
    global face_comparison
    face_comparison.reset()
    content = {'Log': 'Reset correctly performed',
               'similitude_value': face_comparison.face_comparison_result,
               'similitude_value_accumulative': face_comparison.face_comparison_accumulative_result,
               'similitude_value_best': face_comparison.face_comparison_best_result}

    return content, HTTP_200_OK


@app.route('/reset_face_comparison_db', methods=['GET'])
def reset_face_comparison_db():
    global face_comparison_db
    face_comparison_db.reset()
    content = {'Log': 'Reset correctly performed'}

    return content, HTTP_200_OK


@app.route('/reset_check_life', methods=['GET'])
def reset_check_life():
    global face_check_life
    face_check_life.reset()
    content = {'Log': 'Reset correctly performed'}

    return content, HTTP_200_OK


if __name__ == '__main__':
    app.run(debug=True)
