"""
    face_container.py
    ~~~~~~~~~

    This module implements the FaceContainer class

"""

from face_recognition import load_image_file

from src.utils import utils


class FaceContainer(object):
    """
    The class serves as a container for the face_recognition application
    """

    BUFFER_MAX_FRAMES = 8
    LAST_IN_BUFFER = 0

    def __init__(self):
        """
        Initialize the class attributes.
        The self.buffer is a dict that contains three lists. They are treated as a buffer in conjunction, as each
        element in the same position is related.
        """

        self.file_image_path = None
        self.buffer = {'pixels': [],
                       'landmarks': [],
                       'encodings': []}  # Max BUFFER_MAX_FRAMES
        self.pixels_image_tmp = None

    def get_buffer(self):
        """
        Returns the buffer attribute.

        :return: self.buffer
        """

        return self.buffer

    def insert_image_to_buffer(self):
        """
        Inserts the self.pixels_image_tmp into the buffer. In case of being full, it pops the last item of the buffer.

        :return: nothing
        """

        if self.is_buffer_max_len():
            self.pop_last_image_from_buffer()
        self.buffer['pixels'].insert(FaceContainer.LAST_IN_BUFFER, self.pixels_image_tmp)
        self.buffer['landmarks'].insert(FaceContainer.LAST_IN_BUFFER, None)
        self.buffer['encodings'].insert(FaceContainer.LAST_IN_BUFFER, None)

    def is_buffer_max_len(self):
        """
        Returns True when the buffer is full. Otherwise, False.

        :return: bool
        """

        if len(self.buffer['pixels']) == FaceContainer.BUFFER_MAX_FRAMES:
            return True
        return False

    def get_buffer_len(self):
        """
        Gets the buffer length.

        :return: int
        """

        return len(self.buffer['pixels'])

    def pop_last_image_from_buffer(self):
        """
        Pops the last item of the buffer.

        :return: nothing
        """

        self.buffer['pixels'].pop(FaceContainer.BUFFER_MAX_FRAMES - 1)
        self.buffer['landmarks'].pop(FaceContainer.BUFFER_MAX_FRAMES - 1)
        self.buffer['encodings'].pop(FaceContainer.BUFFER_MAX_FRAMES - 1)

    def change_last_landmark(self, new_landmarks):
        """
        Change the last landmarks in the buffer.

        :param new_landmarks: array of extracted landmarks
        :return: nothing
        """

        if self.get_buffer_len() != 0:
            self.buffer['landmarks'][FaceContainer.LAST_IN_BUFFER] = new_landmarks

    def change_last_encodings(self, new_encodings):
        """
        Change the last encoding (extracted features) in the buffer.

        :param new_encodings: array of extracted features
        :return: nothing
        """

        if self.get_buffer_len() != 0:
            self.buffer['encodings'][FaceContainer.LAST_IN_BUFFER] = new_encodings

    def set_image_file_path(self, file_image_path):
        """
        Change the image file path.

        :param file_image_path: str of the file path
        :return: nothing
        """

        self.file_image_path = file_image_path

    def set_pixels_image_from_image_file(self):
        """
        Set pixels from a image file, and inserts into the buffer.

        :return: nothing
        """

        if self.file_image_path is not None:
            if self.file_image_path.lower().endswith('.png'):
                self.pixels_image_tmp = load_image_file(self.file_image_path)
            elif self.file_image_path.lower().endswith('.jpg'):
                self.pixels_image_tmp = load_image_file(self.file_image_path)
            self.insert_image_to_buffer()

    def set_pixels_image_from_data_url(self, data_url):
        """
        Set pixels from a dataURL, and inserts into the buffer.

        :param data_url: str in dataURL format
        :return: nothing
        """

        image_bytes = utils.dataURL_parser(data_url)
        with utils.BytesIO(utils.decode_base64(image_bytes)) as image_bytes:
            self.pixels_image_tmp = load_image_file(image_bytes)
            self.insert_image_to_buffer()
