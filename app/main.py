import tkinter as tk
from gui import FindWordsAppClass
from ttkthemes import ThemedTk
import platform
from constants import CHECK_OS, THEMES_APP


def main() -> None:
    """
    Основная функция для инициализации и запуска
    приложения с использованием темы в зависимости
    от операционной системы.

    Эта функция:
    - Определяет операционную систему пользователя.
    - В зависимости от ОС, задает тему для окна приложения.
    - Создает и запускает экземпляр класса `FindWordsAppClass`,
    который представляет основное окно приложения.

    Возвращаемое значение:
    None

    ************************************************

    The main function for initialization and startup
    applications using the theme depend
    on the operating system.

    This function:
    - Defines the user's operating system.
    - Depending on the OS, sets the theme for the application window.
    - Creates and launches an instance of the `FindWordsAppClass` class,
    which represents the main application window.

    Return value:
    None
    """    
    os_name = platform.system()
    if os_name == CHECK_OS.get("win"):
        root = ThemedTk(theme=THEMES_APP.get("win"))
    elif os_name == CHECK_OS.get("lin"):
        root = ThemedTk(theme=THEMES_APP.get("lin"))
    else:
        root = tk.Tk()
    app = FindWordsAppClass(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()