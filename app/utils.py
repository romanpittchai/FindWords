import base64
import os
import shutil
import tempfile
import zlib

from PIL import Image, ImageTk


def check_tmp_directory_and_file(
        tmp_dir: str,
        make_or_del: bool,
        filename: str = "main_icon.ico",
) -> bool:
    """
    Проверяет существование временной папки и файла внутри неё.

    Аргументы:
    tmp_dir (str): Путь к временной директории.
    make_or_del (bool): Флаг, указывающий, нужно ли создавать
    директорию и проверять файл (True) или просто
    проверять наличие файла (False).
    filename (str, по умолчанию "main_icon.ico"):
    Имя файла, который нужно проверить в директории.

    Возвращает:
    bool: True, если директория существует и файл найден,
    иначе False.

    ************************************************

    Checks the existence of a temporary folder and a file inside it.

    Arguments:
    tmp_dir (str): The path to the temporary directory.
    make_or_del (bool): A flag indicating whether to create
    a directory and check the file (True) or
    just check for the file (False).
    filename (str, by default "main_icon.ico"):
    The name of the file to be checked in the directory.

    Returns:
    bool: True if the directory exists and the file is found,
    otherwise False.
    """

    check_ico_file: bool = False
    if make_or_del:
        if not (os.path.exists(tmp_dir) and os.path.isdir(tmp_dir)):
            os.mkdir(tmp_dir)
        else:
            file_path: str = os.path.join(tmp_dir, filename)
            if os.path.isfile(file_path):
                check_ico_file = True
    else:
        if (os.path.exists(tmp_dir) and os.path.isdir(tmp_dir)):
            check_ico_file = True
    return check_ico_file


def make_icon_app(
        icon: str, icon_name: str,
        icon_format: str, tmp_dir: str
) -> ImageTk.PhotoImage:
    """
    Создает и возвращает объект PhotoImage для иконки приложения.

    Аргументы:
    icon (str): Закодированная строка иконки в base64.
    icon_name (str): Имя иконки.
    icon_format (str): Формат иконки (например, ".ico").
    tmp_dir (str): Путь к временной директории.

    Возвращает:
    ImageTk.PhotoImage: Объект иконки для приложения.

    ************************************************

    Creates and returns a PhotoImage object for the application icon.

    Arguments:
    icon (str): The encoded string of the icon in base64.
    icon_name (str): The name of the icon.
    icon_format (str): The icon format (for example, ".ico").
    tmp_dir (str): The path to the temporary directory.

    Returns:
    ImageTk.PhotoImage: An icon object for the application.
    """

    icon_name_with_format: str = f"{icon_name}{icon_format}"
    for_check_tmp: bool = True
    check_img_file: bool = check_tmp_directory_and_file(
        tmp_dir, for_check_tmp,
        icon_name_with_format
    )
    if not check_img_file:
        fd, icon_path_app = tempfile.mkstemp(suffix=icon_format, dir=tmp_dir)
        with open(fd, "wb") as icon_file:
            icon_file.write(zlib.decompress(base64.b64decode(icon)))
        os.rename(icon_path_app, os.path.join(tmp_dir, icon_name_with_format))
    return ImageTk.PhotoImage(
        Image.open(os.path.join(tmp_dir, icon_name_with_format))
    )


def delete_tmp(tmp_dir: str) -> None:
    """
    Удаляет временную директорию.

    Аргументы:
    tmp_dir (str): Путь к временной директории.

    ************************************************

    Deletes the temporary directory.

    Arguments:
    tmp_dir (str): The path to the temporary directory.
    """

    for_check_tmp: bool = False
    if check_tmp_directory_and_file(tmp_dir, for_check_tmp):
        shutil.rmtree(tmp_dir)
