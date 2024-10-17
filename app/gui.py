import os
import tkinter as tk
from tkinter import ttk
from logic import  find_words_re
from utils import make_icon_app
import platform
from constants import CHECK_OS


class FindWordsAppClass(ttk.Frame):
    def __init__(self, master=None) -> None:        
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)   
        self.create_main_window()
        self.create_menu()
        # Занести проверку в одну функцию.
        # ********************************
        if platform.system() == CHECK_OS["macOS"]:
            self.init_data_for_darwin()
        else:
            self.init_data_for_another()
        # ********************************
        
        self.create_text_widgets()
        self.create_ok_and_exit_btns()

        self.init_mouse_menu()

        self.bind_all("<Escape>", self.on_escape)
        
        self.bind_all("<Button-1>", self.hide_popup)

        

    def create_main_window(self) -> None:  
        self.master.title("Find Words")
        self.master.geometry("600x700")
        icon = make_icon_app()
        self.master.iconphoto(True, icon)
                

    def create_menu(self) -> None:
        self.main_menu = tk.Menu(self.master)
        self.master.config(menu=self.main_menu)
        self.file_menu = tk.Menu(master=self.main_menu, tearoff=0)
        self.file_menu.add_command(label="New file", command=self.new_file)

        self.main_menu.add_cascade(label="File", menu=self.file_menu)

    def init_data_for_darwin(self) -> None:
        self.init_data: dict = {
            "tk_or_ttk": tk,
            "But_2_or_But_3": "<Button-2>",
        }

    def init_data_for_another(self):
        self.init_data: dict = {
            "tk_or_ttk": ttk,
            "But_2_or_But_3": "<Button-3>",
        } 

    def create_text_widgets(self) -> None:
        self.frame_general_txt = ttk.Frame(self.master)
        self.frame_general_txt.pack(side="top", fill="both", expand=True)

        self.frame_ent = ttk.Frame(master=self.frame_general_txt)
        self.frame_ent.pack(side="top", fill="both", expand=True)

        self.frame_under_ent = ttk.Frame(master=self.frame_ent)
        self.frame_under_ent.pack(side="top", fill="y", expand=True)

        self.frame_txt = ttk.Frame(master=self.frame_general_txt)
        self.frame_txt.pack(side="bottom", fill="both", expand=True)
        
        self.ent_widget = self.init_data["tk_or_ttk"].Entry(master=self.frame_under_ent, width=50)
        self.ent_widget.pack(side="left", fill="none", expand=False)
        self.ent_widget.bind("<Control-a>", self.select_all_text)
        
        self.ent_button = ttk.Button(master=self.frame_under_ent, text="The")
        self.ent_button.pack(side="left", fill="none", expand=False)


        self.txt_widget = tk.Text(master=self.frame_txt, wrap="word")
        self.scrollbar_txt = ttk.Scrollbar(master=self.frame_txt, command=self.txt_widget.yview)
        self.txt_widget['yscrollcommand'] = self.scrollbar_txt.set
        self.scrollbar_txt.pack(side="right", fill="y")
        self.txt_widget.pack(side="bottom", fill="both", expand=True)
        self.txt_widget.bind("<Control-a>", self.select_all_text)


    def create_ok_and_exit_btns(self) -> None:
        self.frame_btn_all = ttk.Frame(self.master)
        self.frame_btn_all.pack(side="bottom", fill="both", expand=True)
        self.frame_btn = ttk.Frame(master=self.frame_btn_all)
        self.frame_btn.pack(side="bottom", fill="y", expand=True)
        self.frame_btn_ok = ttk.Frame(master=self.frame_btn)
        self.frame_btn_ok.pack(side="left", fill="both", expand=True,  padx=10, pady=10)
        self.frame_btn_exit = ttk.Frame(master=self.frame_btn)
        self.frame_btn_exit.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        

        self.btn_ok = ttk.Button(master=self.frame_btn_ok, width=10, command=self.find_words)
        self.btn_ok["text"] = "OK"
        #self.btn_ok["command"] = self.find_words()

        self.btn_ok.pack()

        self.btn_exit = ttk.Button(master=self.frame_btn_exit, width=10)
        self.btn_exit["text"] = "Exit"
        #self.btn_exit["command"] = self.com
        self.btn_exit.pack()

        


    def init_mouse_menu(self) -> None:
        self.context_mouse_menu = tk.Menu(self, tearoff=0)
        self.context_mouse_menu.add_command(label="Select text", command=self.select_all_text)
        self.context_mouse_menu.add_command(label="Cut", command=self.cut)
        self.context_mouse_menu.add_command(label="Copy", command=self.copy)
        self.context_mouse_menu.add_command(label="Paste", command=self.paste)

        self.ent_widget.bind(self.init_data["But_2_or_But_3"], self.mouse_popup)
        self.txt_widget.bind(self.init_data["But_2_or_But_3"], self.set_txt_widget_focus)
        self.txt_widget.bind(self.init_data["But_2_or_But_3"], self.mouse_popup)
        self.master.bind(self.init_data["But_2_or_But_3"], self.clear_focus)


    def mouse_popup(self, event) -> None:
        try:
            self.context_mouse_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_mouse_menu.grab_release()

    def hide_popup(self, event) -> None:
        self.context_mouse_menu.unpost()

    def set_txt_widget_focus(self, event) -> None:
        self.focus_set()

    def clear_focus(self, event) -> None:
        self.focus_set()

    def on_escape(self, event) -> None:
        self.hide_popup(event)



    def select_all_text(self) -> None:
        pass

    def cut(self) -> None:
        pass

    def copy(self) -> None:
        pass

    def paste(self) -> None:
        pass

    def new_file(self) -> None:
        pass 


    def find_words(self) -> None:
        text = self.txt_widget.get("1.0", "end-1c")
        print(text)
        pattern = self.ent_widget.get()
        if pattern == "":
            pattern = r'TTN-\d{10}'
        print(pattern)
        find_words_re(pattern, text)


       
