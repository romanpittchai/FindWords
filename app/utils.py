import os
import tempfile
import base64
import zlib
from PIL import Image, ImageTk
from constants import ICON_PLUG, ICON_NAME

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
        print(file_path)
        if os.path.isfile(file_path):
            check_ico_file = True
    return check_ico_file



def make_icon_app() -> ImageTk.PhotoImage:
    icon_plug_app: bytes = zlib.decompress(base64.b64decode(ICON_PLUG))
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    tmp_dir:str = os.path.join(current_dir, 'tmp')
    check_ico_file: bool = check_tmp_directory_and_file(ICON_NAME, tmp_dir)
    
    returning_icon_path: str = os.path.join(tmp_dir, ICON_NAME)
    
    if not check_ico_file:
        fd, icon_path_app = tempfile.mkstemp(suffix=".ico", dir=tmp_dir)
        with open(fd, "wb") as icon_file:
            icon_file.write(icon_plug_app)
        returning_icon_path: str = os.path.join(tmp_dir, ICON_NAME)
        os.rename(icon_path_app, returning_icon_path)
    
    return create_ico(returning_icon_path)

def create_ico(img_path: str) -> ImageTk.PhotoImage:
    """
    Открывает изображение и создает объект PhotoImage для использования в tkinter.

    :param img_path: Путь к изображению, которое нужно открыть.
    :return: Объект PhotoImage, который можно использовать в tkinter.
    """
    image: Image.Image = Image.open(img_path)
    photo: ImageTk.PhotoImage = ImageTk.PhotoImage(image)

    return photo