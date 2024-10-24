import os
import platform
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List

from constants import (CHECK_OS, FILETYPES, ICON_FORMAT, ICON_NAMES, ICONS,
                       MENU_MOUSE_NAME, TMP_DIR, TOOLTIP_DELAY)
from logic import find_words_re
from utils import delete_tmp, make_icon_app


class ToolTip:
    """
    Класс для создания всплывающих подсказок для виджетов.

    Атрибуты:
    widget (tk.Widget): Виджет, для которого создается подсказка.
    text (str): Текст подсказки.
    delay (int): Задержка перед показом подсказки.
    tooltip_window (tk.Toplevel): Окно с подсказкой.
    id_after (str): Идентификатор запланированного показа подсказки.

    ************************************************

    A class for creating tooltips for widgets.

    Attributes:
    widget (tk.Widget): The widget for which the hint is being created.
    text (str): The text of the hint.
    delay (int): The delay before showing the hint.
    tooltip_window (tk.Toplevel): A window with a hint.
    id_after (str): ID of the scheduled hint display.
    """

    def __init__(self, widget, text, delay=TOOLTIP_DELAY) -> None:
        """
        Инициализация подсказки с указанием виджета,
        текста и задержки.

        ************************************************

        Initializing the hint with the widget,
        text, and delay.
        """

        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id_after = None
        self.widget.bind("<Enter>", self.schedule_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def schedule_tooltip(self, event=None) -> None:
        """
        Запланировать показ подсказки с задержкой.

        ************************************************

        Schedule a delayed prompt display.
        """

        self.id_after = self.widget.after(self.delay, self.show_tooltip)

    def show_tooltip(self, event=None) -> None:
        """
        Отобразить подсказку.

        ************************************************

        Show a tooltip.
        """

        if self.tooltip_window or not self.text:
            return

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(
            tw, text=self.text,
            background="white",
            relief="solid",
            borderwidth=1
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None) -> None:
        """
        Скрыть подсказку.

        ************************************************

        Hide tooltip.
        """

        if self.id_after:
            self.widget.after_cancel(self.id_after)
            self.id_after = None
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()


class FindWordsAppClass(ttk.Frame):
    """
    Основной класс приложения для поиска слов, наследуется от ttk.Frame.

    Атрибуты:
    master (tk.Tk): Главный объект Tkinter.
    tmp_folder (str): Временная директория для хранения файлов.
    filepath_open (str): Путь к открытому исходному файлу.
    filepath_save (str): Путь для сохранения обработанного файла.
    filepath_reg_exp_open (str): Путь к файлу с регулярными выражениями.
    filepath_reg_exp_save (str): Путь для сохранения файла с
    регулярными выражениями.

    ************************************************

    The main class of the word search application is inherited from ttk.Frame.

    Attributes:
    master (tk.Tk ): The main object of Tkinter.
    tmp_folder (str): Temporary directory for storing files.
    filepath_open (str): The path to the open source file.
    filepath_save (str): The path to save the processed file.
    filepath_reg_exp_open (str): The path to the regular expression file.
    filepath_reg_exp_save (str): The path to save the regular expression file.
    """

    def __init__(self, master=None) -> None:
        """
        Инициализация основного окна приложения.

        ************************************************

        Initialization of the main application window.
        """

        super().__init__(master)
        self.master = master
        self.tmp_folder = TMP_DIR
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pack(fill="both", expand=True)
        self.create_main_window()
        self.create_menu()
        self.init_data_for_OS()
        self.create_text_widgets()
        self.create_ok_and_exit_btns()
        self.init_mouse_menu()
        self.init_bind_shortcuts()

    def create_main_window(self) -> None:
        """
        Создание основного окна с иконкой и размерами.

        ************************************************

        Creating a main window with an icon and dimensions.
        """

        self.master.title("Find Words")
        self.master.geometry("600x700")
        self.main_icon = make_icon_app(
            ICONS.get("main_icon"),
            ICON_NAMES.get("main_icon"),
            ICON_FORMAT.get("ico"),
            TMP_DIR
        )
        self.master.iconphoto(True, self.main_icon)
        self.filepath_open = None
        self.filepath_save = None
        self.filepath_reg_exp_open = None
        self.filepath_reg_exp_save = None

    def create_menu(self) -> None:
        """
        Создание меню с пунктами File и RegExp.

        ************************************************

        Creating a menu with File and RegExp items.
        """

        self.main_menu = tk.Menu(self.master, name="main_menu")
        self.master.config(menu=self.main_menu)
        self.file_menu = tk.Menu(master=self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(
            label="Open the source file",
            command=self.open_source_file,
            accelerator="Ctrl+O"
        )
        self.master.bind(
            '<Control-o>',
            lambda event: self.open_source_file()
        )
        self.file_menu.add_command(
            label="Start processing",
            command=self.find_words,
            accelerator="Alt+S"
        )
        self.master.bind(
            '<Alt-s>', lambda event: self.find_words()
        )
        self.file_menu.add_command(
            label="Save the processed file",
            command=self.save_file,
            accelerator="Ctrl+S"
        )
        self.master.bind(
            '<Control-s>', lambda event: self.save_file()
        )

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Exit",
            command=self.exit_program,
            accelerator="Ctrl+Q"
        )
        self.master.bind(
            '<Control-q>', lambda event: self.exit_program()
        )

        self.reg_exp_menu = tk.Menu(master=self.main_menu, tearoff=0)
        self.main_menu.add_cascade(
            label="RegExp and Text",
            menu=self.reg_exp_menu
        )
        self.reg_exp_menu.add_command(
            label="Open a file with regexp",
            command=self.open_regexp_file,
            accelerator="Ctrl+Shift+O"
        )
        self.master.bind(
            '<Control-Shift-O>', lambda event: self.open_regexp_file()
        )

        self.reg_exp_menu.add_command(
            label="Save a file with regexp",
            command=self.save_regexp_file,
            accelerator="Ctrl+Shift+S"
        )
        self.master.bind(
            '<Control-Shift-S>', lambda event: self.save_regexp_file()
        )

        self.reg_exp_menu.add_separator()

        self.reg_exp_menu.add_command(
            label="Select text",
            command=self.select_all,
            accelerator="Ctrl+A"
        )
        self.master.bind(
            '<Control-a>', self.select_all
        )

        self.reg_exp_menu.add_command(
            label="Clear the text field",
            command=self.clear_field,
            accelerator="Ctrl+G"
        )
        self.master.bind(
            '<Control-g>', lambda event: self.clear_field()
        )
        self.reg_exp_menu.add_command(
            label="Cut text",
            command=self.cut,
            accelerator="Ctrl+X"
        )
        self.reg_exp_menu.add_command(
            label="Copy text",
            command=self.copy,
            accelerator="Ctrl+C"
        )
        self.reg_exp_menu.add_command(
            label="Paste text",
            command=self.paste,
            accelerator="Ctrl+V"
        )

    def create_text_widgets(self) -> None:
        """
        Создание текстовых полей и привязка к ним прокрутки.

        ************************************************

        Creating text fields and linking scrolling to them.
        """

        self.frame_general_txt = ttk.Frame(self.master)
        self.frame_general_txt.pack(side="top", fill="both", expand=True)

        self.frame_ent = ttk.Frame(master=self.frame_general_txt)
        self.frame_ent.pack(side="top", fill="both", expand=True)

        self.frame_under_ent = ttk.Frame(master=self.frame_ent)
        self.frame_under_ent.pack(side="top", fill="y", expand=True)

        self.frame_txt = ttk.Frame(master=self.frame_general_txt)
        self.frame_txt.pack(side="bottom", fill="both", expand=True)

        self.ent_widget = self.init_data.get("tk_or_ttk").Entry(
            master=self.frame_under_ent, width=50
        )
        self.ent_widget.pack(side="left", fill="none", expand=False)
        ToolTip(self.ent_widget, "RegExp")

        self.ent_button = ttk.Button(
            master=self.frame_under_ent,
            text="Open",
            command=self.open_field_regexp
        )
        self.ent_button.pack(side="left", fill="none", expand=False)
        ToolTip(self.ent_button, "Open regular expression")
        self.txt_widget = tk.Text(master=self.frame_txt, wrap="word")
        self.scrollbar_txt = ttk.Scrollbar(
            master=self.frame_txt,
            command=self.txt_widget.yview
        )
        self.txt_widget['yscrollcommand'] = self.scrollbar_txt.set
        self.scrollbar_txt.pack(side="right", fill="y")
        self.txt_widget.pack(side="bottom", fill="both", expand=True)

    def create_ok_and_exit_btns(self) -> None:
        """
        Создание кнопок 'OK' и 'Exit'.

        ************************************************

        Creating the 'OK' and 'Exit' buttons.
        """

        self.frame_btn_all = ttk.Frame(self.master)
        self.frame_btn_all.pack(
            side="bottom",
            fill="both",
            expand=True
        )
        self.frame_btn = ttk.Frame(master=self.frame_btn_all)
        self.frame_btn.pack(side="bottom", fill="y", expand=True)
        self.frame_btn_ok = ttk.Frame(master=self.frame_btn)
        self.frame_btn_ok.pack(
            side="left", fill="both",
            expand=True,
            padx=10, pady=10
        )
        self.frame_btn_exit = ttk.Frame(master=self.frame_btn)
        self.frame_btn_exit.pack(
            side="right", fill="both",
            expand=True,
            padx=10, pady=10
        )

        self.btn_ok = ttk.Button(
            master=self.frame_btn_ok,
            text="OK", width=10,
            command=self.find_words
        )
        self.btn_ok.pack()
        ToolTip(self.btn_ok, "Start processing")

        self.btn_exit = ttk.Button(
            master=self.frame_btn_exit,
            text="Exit", width=10,
            command=self.exit_program
        )
        self.btn_exit.pack()
        ToolTip(self.btn_exit, "Exit the program")

    def init_bind_shortcuts(self) -> None:
        """
        Инициализация привязки клавиш и горячих клавиш.

        ************************************************

        Initializes key bindings and hotkeys.
        """

        self.bind_all("<Escape>", self.on_escape)
        self.bind_all("<Button-1>", self.hide_popup)

    def init_mouse_menu(self) -> None:
        """
        Инициализация контекстного меню мыши.

        ************************************************

        Initializes the context menu for mouse actions.
        """

        self.context_mouse_menu = tk.Menu(
            self, tearoff=0, name=MENU_MOUSE_NAME
        )
        self.context_mouse_menu.add_command(
            label="Select text",
            command=self.select_all
        )
        self.context_mouse_menu.add_separator()
        self.context_mouse_menu.add_command(
            label="Cut",
            command=self.cut
        )
        self.context_mouse_menu.add_command(
            label="Copy",
            command=self.copy
        )
        self.context_mouse_menu.add_command(
            label="Paste",
            command=self.paste
        )
        self.ent_widget.bind(
            self.init_data.get("But_2_or_But_3"),
            self.mouse_popup, add="+"
        )
        self.ent_widget.bind(
            self.init_data.get("But_2_or_But_3"),
            self.set_txt_widget_focus, add="+"
        )
        self.txt_widget.bind(
            self.init_data.get("But_2_or_But_3"),
            self.mouse_popup, add="+"
        )
        self.txt_widget.bind(
            self.init_data.get("But_2_or_But_3"),
            self.set_txt_widget_focus, add="+"
        )

    def mouse_popup(self, event) -> None:
        """
        Отображение контекстного меню при нажатии кнопки мыши.

        ************************************************

        Displays the context menu when the mouse button is clicked.
        """

        try:
            self.context_mouse_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_mouse_menu.grab_release()

    def hide_popup(self, event) -> None:
        """
        Скрытие контекстного меню.

        ************************************************

        Hides the context menu.
        """

        full_widget_name: str = str(event.widget)
        widget_name: List[str] = full_widget_name.split('.')[-1]
        if not widget_name == MENU_MOUSE_NAME:
            self.context_mouse_menu.unpost()

    def set_txt_widget_focus(self, event) -> None:
        """
        Установка фокуса на текстовый виджет.

        ************************************************

        Sets the focus on the text widget.
        """

        event.widget.focus_set()

    def on_escape(self, event) -> None:
        """
        Обработка события 'Escape' для скрытия контекстного меню.

        ************************************************

        Handles the 'Escape' event to hide the context menu.
        """

        self.hide_popup(event)

    def init_data_for_OS(self) -> None:
        """
        Инициализация данных в зависимости от операционной системы.

        ************************************************

        Initializes data based on the operating system.
        """

        if platform.system() == CHECK_OS.get("macOS"):
            self.init_data: dict = {
                "tk_or_ttk": tk,
                "But_2_or_But_3": "<Button-2>",
            }
        else:
            self.init_data: dict = {
                "tk_or_ttk": ttk,
                "But_2_or_But_3": "<Button-3>",
            }

    def open_field_regexp(self) -> None:
        """
        Открытие окна для редактирования регулярных выражений.

        ************************************************

        Opens a window to edit regular expressions.
        """

        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Regular Expression")
        self.new_window.geometry("500x600")

        self.txt_regexp_widget = tk.Text(self.new_window, wrap="word")
        self.scrollbar_txt_regexp = ttk.Scrollbar(
            master=self.new_window,
            command=self.txt_regexp_widget.yview
        )
        self.txt_regexp_widget['yscrollcommand'] = (
            self.scrollbar_txt_regexp.set
        )
        self.scrollbar_txt_regexp.pack(side="right", fill="y")
        self.txt_regexp_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self.txt_regexp_widget.insert("1.0", self.ent_widget.get())

        self.ok_regexp_button = ttk.Button(
            self.new_window, text="OK",
            command=self.save_and_close
        )
        self.ok_regexp_button.pack(pady=10)

        self.create_context_menu(self.txt_regexp_widget)

    def save_and_close(self) -> None:
        """
        Сохранение изменений и закрытие окна.

        ************************************************

        Saves changes and closes the window.
        """

        edited_text = self.txt_regexp_widget.get("1.0", "end-1c")
        self.ent_widget.delete(0, tk.END)
        self.ent_widget.insert(0, edited_text)
        self.new_window.destroy()

    def create_context_menu(self, text_widget) -> None:
        """
        Создание контекстного меню для текстового виджета.

        ************************************************

        Creates a context menu for the text widget.
        """

        self.context_regexp_mouse_menu = tk.Menu(self, tearoff=0)
        self.context_regexp_mouse_menu.add_command(
            label="Select text", command=lambda: self.select_all()
        )
        text_widget.bind(
            '<Control-a>', self.select_all
        )
        self.context_regexp_mouse_menu.add_separator()
        self.context_regexp_mouse_menu.add_command(
            label="Cut", command=lambda: self.cut()
        )
        self.context_regexp_mouse_menu.add_command(
            label="Copy", command=lambda: self.copy()
        )
        self.context_regexp_mouse_menu.add_command(
            label="Paste", command=lambda: self.paste()
        )
        text_widget.bind(
            self.init_data.get("But_2_or_But_3"),
            self.show_reg_exp_context_menu
        )

    def show_reg_exp_context_menu(self, event) -> None:
        """
        Отображение контекстного меню регулярных выражений.

        ************************************************

        Displays the context menu for regular expressions.
        """

        self.context_regexp_mouse_menu.tk_popup(event.x_root, event.y_root)

    def get_active_widget(self) -> None:
        """
        Возвращает активный виджет в фокусе.

        ************************************************

        Returns the currently focused widget.
        """

        return self.focus_get()

    def select_all(self, event=None) -> None:
        """
        Выбор всего текста в активном виджете.

        ************************************************

        Selects all text in the active widget.
        """

        widget = self.get_active_widget()
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end-1c")
        elif isinstance(widget, tk.Entry):
            widget.select_range(0, tk.END)
            widget.icursor(tk.END)

    def cut(self, event=None) -> None:
        """
        Вырезает выделенный текст из активного виджета.

        ************************************************

        Cuts the selected text from the active widget.
        """

        self.master.focus_get().event_generate("<<Cut>>")

    def copy(self, event=None) -> None:
        """
        Копирует выделенный текст из активного виджета.

        ************************************************

        Copies the selected text from the active widget.
        """

        self.master.focus_get().event_generate("<<Copy>>")

    def paste(self, event=None) -> None:
        """
        Вставляет текст в активный виджет.

        ************************************************

        Pastes text into the active widget.
        """

        self.master.focus_get().event_generate("<<Paste>>")

    def clear_field(self) -> None:
        """
        Очищает поле в активном текстовом виджете.

        ************************************************

        Clears the field in the active text widget.
        """

        widget = self.get_active_widget()
        if isinstance(widget, tk.Text):
            widget.delete("1.0", "end")
        elif isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)

    def open_regexp_file(self) -> None:
        """
        Открытие файла для чтения регулярных выражений.

        ************************************************

        Opens a file to read regular expressions.
        """

        self.filepath_reg_exp_open: str = (
            filedialog.askopenfilename(
                filetypes=FILETYPES,
                defaultextension=''
            )
        )
        if self.filepath_reg_exp_open:
            self.ent_widget.delete(0, tk.END)
            with open(self.filepath_reg_exp_open, "r") as out_reg_exp_file:
                text_reg_exp: str = out_reg_exp_file.read()
                self.filepath_reg_exp_open = None
            self.ent_widget.insert(0, text_reg_exp)

    def save_regexp_file(self) -> None:
        """
        Сохранение регулярных выражений в файл.

        ************************************************

        Saves the regular expressions to a file.
        """
        if CHECK_OS.get("win"):
            self.filepath_reg_exp_save = (
                filedialog.asksaveasfilename(
                    filetypes=FILETYPES,
                    defaultextension='initialfile'
                )
            )
        else:
            self.filepath_reg_exp_save = (
                filedialog.asksaveasfilename(
                    filetypes=FILETYPES
                )
            )
        if self.filepath_reg_exp_save:
            with open(self.filepath_reg_exp_save, "w") as in_reg_exp_file:
                in_reg_exp_file.write(self.ent_widget.get())

            self.filepath_reg_exp_save = None

    def open_source_file(self) -> None:
        """
        Открытие исходного файла для обработки.

        ************************************************

        Opens a source file for processing.
        """

        self.filepath_open: str = (
            filedialog.askopenfilename(
                filetypes=FILETYPES,
                defaultextension=''
            )
        )
        if self.filepath_open:
            self.txt_widget.delete("1.0", tk.END)
            self.txt_widget.insert("1.0", (f"Open file: {self.filepath_open}"))

    def save_file(self) -> None:
        """
        Сохранение текста в файл.

        ************************************************

        Saves the text to a file.
        """
        if CHECK_OS.get("win"):
            self.filepath_save = (
                filedialog.asksaveasfilename(
                    filetypes=FILETYPES,
                    defaultextension='initialfile'
                )
            )
        else:
            self.filepath_save = (
                filedialog.asksaveasfilename(
                    filetypes=FILETYPES
                )
            )
        if self.filepath_save:
            with open(self.filepath_save, "w") as in_file:
                in_file.write(self.txt_widget.get("1.0", "end-1c"))

            self.filepath_save = None

    def find_words(self) -> None:
        """
        Поиск слов в тексте с использованием регулярных выражений.

        ************************************************

        Finds words in the text using regular expressions.
        """

        pattern: str = self.ent_widget.get()
        if not pattern:
            messagebox.showinfo(
                "Error",
                "The regular expression is not set."
            )
            return
        if not self.filepath_open:
            all_text = self.txt_widget.get("1.0", "end-1c")
        else:
            with open(self.filepath_open, "r") as out_file:
                all_text = out_file.read()
                self.filepath_open = None
        result = "\n".join(find_words_re(pattern, all_text))
        self.txt_widget.delete("1.0", tk.END)
        self.txt_widget.insert("1.0", result)

    def exit_program(self) -> None:
        """
        Завершение программы и закрытие окна.

        ************************************************

        Exits the program and closes the window.
        """

        self.master.title("Program is closing")
        delete_tmp(TMP_DIR)
        self.master.destroy()

    def on_closing(self) -> None:
        """
        Закрытие программы и удаление временных файлов.

        ************************************************

        Closes the program and deletes temporary files.
        """

        if self.tmp_folder and os.path.exists(self.tmp_folder):
            shutil.rmtree(self.tmp_folder)
        self.master.destroy()
