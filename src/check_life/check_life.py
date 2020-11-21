from face_recognition import face_landmarks
from numpy import asarray, append

from src.face_container.face_container import FaceContainer


class Checklife(FaceContainer):
    MINIMUM_FACES_LANDMARKED_TO_CHECK_LIFE = FaceContainer.BUFFER_MAX_FRAMES - 3

    def __init__(self):
        FaceContainer.__init__(self)
        self.status_check_life = asarray([])

    def reset(self):
        self.__init__()

    def set_landmarks_for_all_faces_in_buffer(self):
        if self.is_buffer_max_len():
            for index, pixels in enumerate(reversed(self.buffer['pixels'])):
                self.buffer['landmarks'][index] = self.get_face_landmarks_from_pixels(pixels, model='small')
            self.remove_none_landmarks()
        else:
            return None

    def remove_none_landmarks(self):
        tmp_pixels, tmp_landmarks, tmp_encoding = [], [], []
        for index, tmp_landmark in enumerate(self.buffer['landmarks']):
            if tmp_landmark:
                tmp_pixels.append(self.buffer['pixels'][index])
                tmp_landmarks.append(self.buffer['landmarks'][index])
                tmp_encoding.append(self.buffer['encodings'][index])
        self.buffer['pixels'] = tmp_pixels
        self.buffer['landmarks'] = tmp_landmarks
        self.buffer['encodings'] = tmp_encoding

    def check_if_left_move(self):
        buffer_len = self.check_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACES_LANDMARKED_TO_CHECK_LIFE:
            for index in range(buffer_len - 1):
                if self.buffer['landmarks'][index][0]['nose_tip'][0][0] <= \
                        self.buffer['landmarks'][index + 1][0]['nose_tip'][0][0]:
                    self.status_check_life = append(self.status_check_life, True)
                else:
                    self.status_check_life = append(self.status_check_life, False)
            if self.status_check_life.all():
                return True
            return False
        return None

    def check_if_right_move(self):
        buffer_len = self.check_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACES_LANDMARKED_TO_CHECK_LIFE:
            for index in range(buffer_len - 1):
                if self.buffer['landmarks'][index][0]['nose_tip'][0][0] >= \
                        self.buffer['landmarks'][index + 1][0]['nose_tip'][0][0]:
                    self.status_check_life = append(self.status_check_life, True)
                else:
                    self.status_check_life = append(self.status_check_life, False)
            if self.status_check_life.all():
                return True
            return False
        return None

    def check_if_top_move(self):
        buffer_len = self.check_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACES_LANDMARKED_TO_CHECK_LIFE:
            for index in range(buffer_len - 1):
                if self.buffer['landmarks'][index][0]['nose_tip'][0][1] >= \
                        self.buffer['landmarks'][index + 1][0]['nose_tip'][0][1]:
                    self.status_check_life = append(self.status_check_life, True)
                else:
                    self.status_check_life = append(self.status_check_life, False)
            if self.status_check_life.all():
                return True
            return False
        return None

    def check_if_bot_move(self):
        buffer_len = self.check_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACES_LANDMARKED_TO_CHECK_LIFE:
            for index in range(buffer_len - 1):
                if self.buffer['landmarks'][index][0]['nose_tip'][0][1] <= \
                        self.buffer['landmarks'][index + 1][0]['nose_tip'][0][1]:
                    self.status_check_life = append(self.status_check_life, True)
                else:
                    self.status_check_life = append(self.status_check_life, False)
            if self.status_check_life.all():
                return True
            return False
        return None

    def set_and_extract_first_landmarks(self, model='large'):
        self.change_last_landmark(self.get_face_landmarks_from_pixels(self.buffer['pixels'][0], model))
        return None

    @staticmethod
    def get_face_landmarks_from_pixels(pixels, model='large'):
        return face_landmarks(pixels, model=model)


if __name__ == "__main__":
    test_images = ['../test_files/test_data/Cara_1.jpg',
                   '../test_files/test_data/Cara_2.jpg',
                   '../test_files/test_data/Cara_3.jpg',
                   '../test_files/test_data/Cara_4.jpg',
                   '../test_files/test_data/Cara_5.jpg',
                   '../test_files/test_data/Cara_6.jpg']

    obj_check_life = Checklife()
    for test_image in test_images:
        obj_check_life.set_image_file_path(test_image)
        obj_check_life.set_pixels_image_from_image_file()
        obj_check_life.set_landmarks_for_all_faces_in_buffer()
    print(obj_check_life.check_if_left_move())
