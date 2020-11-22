"""
    face_comparison.py
    ~~~~~~~~~

    This module implements the FaceComparison class

"""

from face_recognition import face_encodings
from numpy import corrcoef, ndarray, asarray, average, append

from src.face_container.face_container import FaceContainer


class FaceComparison(FaceContainer):
    """
    The class conducts the face comparison (DNI vs face) for the face_recognition application. (FaceContainer class)
    """

    def __init__(self):
        """
        Initialize the class attributes.
        """

        FaceContainer.__init__(self)
        self.dni_person_encoding = None

        self.face_comparison_result = None
        self.face_comparison_result_array = asarray([])
        self.face_comparison_accumulative_result = None
        self.face_comparison_best_result = None

    def reset(self):
        """
        Resets the object.
        """

        self.__init__()

    def extract_face_128d_features_from_single_photo(self):
        """
        Extracts the features for each face in the image.

        :return: nothing
        """

        self.dni_person_encoding = face_encodings(self.pixels_image_tmp)

    def compare_encoded_faces(self):
        """
        Extracts the features for each face in the image.

        :return: nothing
        """

        self.face_comparison_result = None
        # Limits that 2 faces are in the image (DNI and person face)
        if len(self.dni_person_encoding) == 2:
            if isinstance(self.dni_person_encoding[0], ndarray) and isinstance(self.dni_person_encoding[1], ndarray):
                self.face_comparison_result = round(corrcoef(self.dni_person_encoding[0],
                                                             self.dni_person_encoding[1])[0, 1] * 100, 2)
                self.face_comparison_result_array = append(self.face_comparison_result_array,
                                                           self.face_comparison_result)
                self.face_comparison_accumulative_result = round(average(self.face_comparison_result_array), 2)
                self.face_comparison_best_result = max(self.face_comparison_result_array)


if __name__ == '__main__':
    """
    To test that all functions are working fine.
    """
    # dataURL = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    # obj_face_comp = FaceComp()
    # obj_face_comp.set_pixels_image_from_data_url(dataURL)

    obj_face_comp = FaceComparison()
    photo = '../test_files/test_data/norb_dnii.jpg'
    obj_face_comp.set_image_file_path(photo)
    obj_face_comp.set_pixels_image_from_image_file()

    obj_face_comp.extract_face_128d_features_from_single_photo()
    obj_face_comp.compare_encoded_faces()
    print(obj_face_comp.face_comparison_result)
