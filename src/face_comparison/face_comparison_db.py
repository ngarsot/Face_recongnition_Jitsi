"""
    face_comparison_db.py
    ~~~~~~~~~

    This module implements the FaceComparisonDB class

"""

import ntpath

from face_recognition import face_encodings
from numpy import corrcoef, ndarray, linalg

from src.face_container.face_container import FaceContainer
from src.utils.utils_db import *


class FaceComparisonDB(FaceContainer):
    """
    The class conducts the face comparison DB (face vs DB) for the face_recognition application. (FaceContainer class)
    """

    def __init__(self):
        """
        Initialize the class attributes.
        """

        FaceContainer.__init__(self)
        self.person_pixels = None
        self.person_encoding = None
        self.person_possible_identified = 'Unknown'
        self.unknown_pixels = None
        self.unknown_encoding = None
        self.unknown_name = None

        self.face_comparison_current_result_distance = 100000
        self.face_comparison_best_result_distance = 100000
        self.face_comp_best_result_pearson = 0

    def reset(self):
        """
        Resets the object.
        """

        self.__init__()

    def encoding_person(self, data_url=None, image_path=None):
        """
        Extracts the features of the faces in an image or a dataURL.

        :param data_url: str of dataURL format
        :param image_path: str of the image file path
        :return: nothing
        """

        # Loads the pixels from an image or a dataURL
        if data_url is not None:
            self.set_pixels_image_from_data_url(data_url)
        elif image_path is not None:
            self.set_image_file_path(image_path)
            self.set_pixels_image_from_image_file()
        self.person_pixels = self.pixels_image_tmp
        # Extracts the features of the faces
        self.person_encoding = self.extract_face_128d_features_from_single_photo(self.person_pixels)

    def encoding_unknown(self, image_path):
        """
        Extracts the features of the faces in an image and sets the name of the person from the image file name.

        :param image_path: str of the image file path (The image file has to contain the person's name)
        :return: nothing
        """

        self.set_image_file_path(image_path)
        self.set_pixels_image_from_image_file()
        self.unknown_pixels = self.pixels_image_tmp
        self.unknown_encoding = self.extract_face_128d_features_from_single_photo(self.unknown_pixels)
        self.unknown_name = ntpath.basename(os.path.splitext(self.file_image_path)[0])

    def load_encoding_unknown_from_db(self, db_dir, threshold=0.6):
        """
        Compares the encoded person face with all the encoded faces in DB. It returns the best result
        whether the result is less than the selected threshold

        :param db_dir: str --> Database path
        :param threshold: int --> the threshold (euclidean distance)
        :return: nothing
        """

        db_rows = get_rows(db_dir)
        for row in db_rows:
            self.unknown_name = row[1]
            self.unknown_encoding = row[2]
            self.compare_encodings(threshold)

    def compare_encodings(self, threshold=0.6):
        """
        Compares two extracted features and sets the result accuracy in % (similitude between extracted faces
        features).

        :param threshold: int --> threshold of comparison in euclidean distance
        :return: nothing
        """
        if self.person_encoding is not None and self.unknown_encoding is not None:
            if isinstance(self.person_encoding, list):
                self.person_encoding = self.person_encoding[0]
            if isinstance(self.unknown_encoding, list):
                self.unknown_encoding = self.unknown_encoding[0]

            if isinstance(self.person_encoding, ndarray) and isinstance(self.unknown_encoding, ndarray):
                self.face_comparison_current_result_distance = linalg.norm(
                    self.person_encoding - self.unknown_encoding)

                if self.face_comparison_current_result_distance <= threshold:
                    self.face_comparison_best_result_distance = min(self.face_comparison_current_result_distance,
                                                                    self.face_comparison_best_result_distance)
                    if self.face_comparison_current_result_distance == self.face_comparison_best_result_distance:
                        self.person_possible_identified = self.unknown_name
                        self.face_comp_best_result_pearson = round(corrcoef(self.person_encoding,
                                                                            self.unknown_encoding)[0, 1] * 100, 2)

    @staticmethod
    def extract_face_128d_features_from_single_photo(pixels_face_to_encode):
        """
        The method extracts the faces features from a single image and a single person.

        :param pixels_face_to_encode: array of pixels
        :return: array with the encoded face (extracted features). None in case of more than 1 face encoded.
        """

        face_encoded = face_encodings(pixels_face_to_encode)
        # Limits the number of face to be 1.
        if len(face_encoded) != 1:
            return None
        return face_encoded


if __name__ == '__main__':
    """
    To test that all functions are working fine.
    """

    obj_face_comp_db = FaceComparisonDB()
    path_db = '../test_files/test_data/db/'
    photo = '../test_files/test_data/Norbert_25anys_frontal_24.png'
    obj_face_comp_db.encoding_person(image_path=photo)

    for photo in os.listdir(path_db):
        photo_path = os.path.join(path_db, photo)
        obj_face_comp_db.encoding_unknown(image_path=photo_path)
        obj_face_comp_db.compare_encodings()

    print('\n\n' + obj_face_comp_db.person_possible_identified + ' wins with ' +
          str(obj_face_comp_db.face_comp_best_result_pearson) + '% of maximum accuracy!!!')
