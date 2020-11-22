"""
    check_life.py
    ~~~~~~~~~

    This module implements the Checklife class

"""

from face_recognition import face_landmarks
from numpy import asarray, append

from src.face_container.face_container import FaceContainer


class Checklife(FaceContainer):
    """
    The class conducts the check life for the face_recognition application. (FaceContainer class)
    """

    MINIMUM_FACE_LANDMARK_TO_CHECK_LIFE = FaceContainer.BUFFER_MAX_FRAMES - 3

    def __init__(self):
        """
        Initialize the class attributes.
        """

        FaceContainer.__init__(self)
        self.status_check_life = asarray([])

    def reset(self):
        """
        Resets the object.
        """

        self.__init__()

    def set_landmarks_for_all_faces_in_buffer(self):
        """
        Generates and stores the landmarks for all the faces in the buffer and into the buffer.

        :return: None in case of not being full the buffer
        """

        if self.is_buffer_max_len():
            for index, pixels in enumerate(reversed(self.buffer['pixels'])):
                self.buffer['landmarks'][index] = self.get_face_landmarks_from_pixels(pixels, model='small')
            self.remove_none_landmarks()
        else:
            return None

    def remove_none_landmarks(self):
        """
        Remove all the items in the buffer that are None.

        :return: nothing
        """

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
        """
        Analyses the head movement. It return True whether the head movement was to the left side.

        :return: bool
        """

        buffer_len = self.get_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACE_LANDMARK_TO_CHECK_LIFE:
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
        """
        Analyses the head movement. It return True whether the head movement was to the right side.

        :return: bool
        """

        buffer_len = self.get_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACE_LANDMARK_TO_CHECK_LIFE:
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
        """
        Analyses the head movement. It return True whether the head movement was to the top side.

        :return: bool
        """

        buffer_len = self.get_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACE_LANDMARK_TO_CHECK_LIFE:
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
        """
        Analyses the head movement. It return True whether the head movement was to the bottom side.

        :return: bool
        """

        buffer_len = self.get_buffer_len()
        if buffer_len > Checklife.MINIMUM_FACE_LANDMARK_TO_CHECK_LIFE:
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
        """
        Returns the face landmarks

        :param pixels: array --> pixels of an image
        :param model: str --> large (64 landmarks) or small (5 landmarks)
        :return: array containing the landmark
        """

        return face_landmarks(pixels, model=model)


if __name__ == "__main__":
    """
    Test purpose for all functions are working fine.
    """

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
