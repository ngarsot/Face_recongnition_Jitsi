from face_recognition import load_image_file

from src.utils import utils


class FaceContainer(object):
    BUFFER_MAX_FRAMES = 8
    LAST_IN_BUFFER = 0

    def __init__(self):
        self.file_image_path = None
        self.buffer = {'pixels': [],
                       'landmarks': [],
                       'encodings': []}  # Max Checklife.MAX_BUFFER_FRAMES frames
        self.pixels_image_tmp = None

    def get_buffer(self):
        return self.buffer

    def insert_image_to_buffer(self):
        if self.is_buffer_max_len():
            self.pop_last_image_from_buffer()
        self.buffer['pixels'].insert(FaceContainer.LAST_IN_BUFFER, self.pixels_image_tmp)
        self.buffer['landmarks'].insert(FaceContainer.LAST_IN_BUFFER, None)
        self.buffer['encodings'].insert(FaceContainer.LAST_IN_BUFFER, None)

    def is_buffer_max_len(self):
        if len(self.buffer['pixels']) == FaceContainer.BUFFER_MAX_FRAMES:
            return True
        return False

    def check_buffer_len(self):
        return len(self.buffer['pixels'])

    def pop_last_image_from_buffer(self):
        self.buffer['pixels'].pop(FaceContainer.BUFFER_MAX_FRAMES - 1)
        self.buffer['landmarks'].pop(FaceContainer.BUFFER_MAX_FRAMES - 1)
        self.buffer['encodings'].pop(FaceContainer.BUFFER_MAX_FRAMES - 1)

    def change_last_landmark(self, new_landmarks):
        if self.check_buffer_len() != 0:
            self.buffer['landmarks'][FaceContainer.LAST_IN_BUFFER] = new_landmarks

    def change_last_encodings(self, new_encodings):
        if self.check_buffer_len() != 0:
            self.buffer['encodings'][FaceContainer.LAST_IN_BUFFER] = new_encodings

    def set_image_file_path(self, file_image_path):
        self.file_image_path = file_image_path

    def set_pixels_image_from_image_file(self):
        if self.file_image_path is not None:
            if self.file_image_path.lower().endswith('.png'):
                self.pixels_image_tmp = load_image_file(self.file_image_path)
            elif self.file_image_path.lower().endswith('.jpg'):
                self.pixels_image_tmp = load_image_file(self.file_image_path)
            self.insert_image_to_buffer()

    def set_pixels_image_from_data_url(self, data_url):
        image_bytes = utils.dataURL_parser(data_url)
        with utils.BytesIO(utils.decode_base64(image_bytes)) as image_bytes:
            self.pixels_image_tmp = load_image_file(image_bytes)
            self.insert_image_to_buffer()
