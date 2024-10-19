import os
import tempfile
import base64
import zlib
from PIL import Image, ImageTk

def check_tmp_directory_and_file(filename: str, tmp_dir: str) -> bool:
    """
    Проверяет наличие папки 'tmp' и указанного файла в ней.

    :param filename: Имя файла для проверки в папке 'tmp'.
    :return: None
    """
    check_ico_file: bool = False
    if not (os.path.exists(tmp_dir) and os.path.isdir(tmp_dir)):
        os.mkdir(tmp_dir)
    else:
        file_path: str = os.path.join(tmp_dir, filename)
        if os.path.isfile(file_path):
            check_ico_file = True
    return check_ico_file


def make_icon_app(icon: str, icon_name: str, icon_format: str) -> ImageTk.PhotoImage:
    tmp_dir: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
    icon_name_with_format: str = f"{icon_name}{icon_format}"
    check_img_file: bool = check_tmp_directory_and_file(icon_name_with_format, tmp_dir)
    if not check_img_file:
        fd, icon_path_app = tempfile.mkstemp(suffix=icon_format, dir=tmp_dir)
        with open(fd, "wb") as icon_file:
            icon_file.write(zlib.decompress(base64.b64decode(icon)))
        os.rename(icon_path_app, os.path.join(tmp_dir, icon_name_with_format))
    return ImageTk.PhotoImage(Image.open(os.path.join(tmp_dir, icon_name_with_format)))
