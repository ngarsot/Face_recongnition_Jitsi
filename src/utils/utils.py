"""
    utils.py
    ~~~~~~~~~

    This module implements all the utils functions.

"""

from base64 import decodebytes
from io import BytesIO
from os import path, getcwd

from face_recognition import load_image_file


def dataURL_parser(data_url):
    """
    This function parsers the dataURL and returns the encoded content in string format.

    :param data_url: str --> dataURL format. Example: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    :return: str --> content of the dataURL content
    """

    content = data_url.split(';')[1]
    return content.split(',')[1]


def decode_base64(encoded):
    """
    Decode from base64 to bytes object.

    :param encoded: str --> "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    :return: bytes object
    """

    return decodebytes(encoded.encode('utf-8'))


def dataURL_to_png(data_url, file_path=None):
    """
    Decode from base64 to bytes object.

    :param encoded: str --> "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    :return: bytes object
    """

    if not file_path:
        file_path = path.join(getcwd(), 'tmp.png')
    with open(file_path, 'wb') as img:
        img.write(decode_base64(dataURL_parser(data_url)))


if __name__ == '__main__':
    """
    Test purpose for all functions are working fine.
    """
    save_image = False

    dataURL = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    image_bytes = dataURL_parser(dataURL)
    with BytesIO(decode_base64(image_bytes)) as image_bytes:
        im = load_image_file(image_bytes)
    if save_image:
        dataURL_to_png(dataURL)
