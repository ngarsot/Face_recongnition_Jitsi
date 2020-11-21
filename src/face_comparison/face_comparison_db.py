import ntpath
import os

from face_recognition import face_encodings
from numpy import corrcoef, ndarray

from src.face_container.face_container import FaceContainer


class FaceComparisonDB(FaceContainer):
    def __init__(self):
        FaceContainer.__init__(self)
        self.person_pixels = None
        self.person_encoding = None
        self.person_possible_identified = 'Unknown'
        self.unknown_pixels = None
        self.unknown_encoding = None
        self.unknown_name = None

        self.face_comparison_current_result = 0
        self.face_comparison_best_result = 0

    def reset(self):
        self.__init__()

    def encoding_person(self, data_url=None, image_path=None):
        if data_url is not None:
            self.set_pixels_image_from_data_url(data_url)
        elif image_path is not None:
            self.set_image_file_path(image_path)
            self.set_pixels_image_from_image_file()
        self.person_pixels = self.pixels_image_tmp
        self.person_encoding = self.extract_face_128d_features_from_single_photo(self.person_pixels)

    def encoding_unknown(self, image_path):
        self.set_image_file_path(image_path)
        self.set_pixels_image_from_image_file()
        self.unknown_pixels = self.pixels_image_tmp
        self.unknown_encoding = self.extract_face_128d_features_from_single_photo(self.unknown_pixels)
        self.unknown_name = ntpath.basename(os.path.splitext(self.file_image_path)[0])

    def compare_encodings(self, threshold=91):
        if self.person_encoding is not None and self.unknown_encoding is not None:
            if isinstance(self.person_encoding[0], ndarray) and isinstance(self.unknown_encoding[0], ndarray):
                self.face_comparison_current_result = round(corrcoef(self.person_encoding[0],
                                                                     self.unknown_encoding[0])[0, 1] * 100, 2)
                if self.face_comparison_current_result >= threshold:
                    self.face_comparison_best_result = max(self.face_comparison_current_result,
                                                           self.face_comparison_best_result)
                    # print('\t-Current --> ' + str(self.face_comparison_current_result))
                    if self.face_comparison_current_result == self.face_comparison_best_result:
                        self.person_possible_identified = self.unknown_name

    @staticmethod
    def extract_face_128d_features_from_single_photo(pixels_face_to_encode):
        face_encoded = face_encodings(pixels_face_to_encode)
        if len(face_encoded) != 1:
            return None
        return face_encoded


if __name__ == '__main__':
    """
    To test that all functions are working fine.
    """

    obj_face_comp_db = FaceComparisonDB()
    path_db = '../test_files/test_data/db/'
    photo = '../test_files/test_data/Norbert_original.png'
    obj_face_comp_db.encoding_person(image_path=photo)
    for photo in os.listdir(path_db):
        photo_path = os.path.join(path_db, photo)
        obj_face_comp_db.encoding_unknown(image_path=photo_path)
        obj_face_comp_db.compare_encodings()

    print('\n\n' + obj_face_comp_db.person_possible_identified + ' wins with ' +
          str(obj_face_comp_db.face_comparison_best_result) + '% of maximum accuracy!!!')
