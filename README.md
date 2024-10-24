# FindWords

FindWords — это приложение для поиска слов в тексте с возможностью использования регулярных выражений. Оно разработано с использованием `Tkinter` и позволяет пользователям загружать текстовые файлы, искать слова, копировать/вставлять текст и сохранять результаты.

## Возможности

- Поиск слов по регулярным выражениям.
- Поддержка работы с текстом через контекстное меню.
- Копирование, вырезание, вставка, выделение текста.
- Поддержка горячих клавиш (Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X).
- Работа с текстовыми файлами через диалоговые окна.

## Требования

- Python 3.9
- Tkinter
- Pillow (для работы с изображениями в Tkinter)

## Установка

1. Клонируйте репозиторий на ваш локальный компьютер:

    ```bash
    git clone <ссылка-на-репозиторий>
    cd FindWords
    ```

2. Установите необходимые зависимости в виртуальном окружении:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    # Или для Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Запуск приложения

Для запуска приложения локально:

```bash
python3 ./app/main.py
```

# Сборка в исполняемый файл

```bash
pip install pyinstaller
pyinstaller --onefile --hidden-import=PIL._tkinter_finder --paths=/путь/к/вашему/venv/lib/python3/site-packages ./app/main.py ./app/utils.py ./app/logic.py ./app/gui.py ./app/constants.py
```

# Лицензия

Этот проект распространяется под лицензией MIT. Для получения дополнительной информации см. файл LICENSE.

----------------------------

# FindWords

FindWords is an application for searching words in text with the ability to use regular expressions. It is developed using `Tkinter` and allows users to load text files, search for words, copy/paste text, and save results.

## Features

- Search for words using regular expressions.
- Support for text manipulation through a context menu.
- Cut, copy, paste, and select text functionalities.
- Support for keyboard shortcuts (Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X).
- File handling for text files via dialog windows.

## Requirements

- Python 3.9
- Tkinter
- Pillow (for working with images in Tkinter)

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository-link>
    cd FindWords
    ```

2. Install the required dependencies in a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # Or for Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Running the Application

To run the application locally:

```bash
python3 ./app/main.py
```

# Building an Executable

```bash
pip install pyinstaller
pyinstaller --onefile --hidden-import=PIL._tkinter_finder --paths=/path/to/your/venv/lib/python3/site-packages ./app/main.py ./app/utils.py ./app/logic.py ./app/gui.py ./app/constants.py
```

# License

Feel free to adjust any parts of the text as needed!
