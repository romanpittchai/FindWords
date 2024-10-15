import tkinter as tk
from tkinter import ttk
from logic import  find_words_re


class FindWordsAppClass(ttk.Frame):
    def __init__(self, master=None) -> None:        
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)      
        self.create_main_window()
        self.create_menu()
        self.create_text_widgets()
        self.create_ok_and_exit_btns()
        

    def create_main_window(self) -> None:
        self.master.title("Find Words")
        self.master.geometry("550x700")

    def create_menu(self) -> None:
        self.main_menu = tk.Menu(self.master)
        self.master.config(menu=self.main_menu)
        self.file_menu = tk.Menu(master=self.main_menu, tearoff=0)
        self.file_menu.add_command(label="New file", command=self.new_file)

        self.main_menu.add_cascade(label="File", menu=self.file_menu)


    def create_text_widgets(self) -> None:
        self.frame_general_txt = ttk.Frame(self.master)
        self.frame_general_txt.pack(side="top", fill="both", expand=True)

        self.frame_ent = ttk.Frame(master=self.frame_general_txt)
        self.frame_ent.pack(side="top", fill="both", expand=True)
        
        self.ent_widget = ttk.Entry(master=self.frame_ent, width=50)
        self.ent_widget.pack(side="top", fill="none", expand=False)

        self.frame_txt = ttk.Frame(master=self.frame_general_txt)
        self.frame_txt.pack(side="bottom", fill="both", expand=True)

        self.txt_widget = tk.Text(master=self.frame_txt, wrap="word")
        self.scrollbar_txt = ttk.Scrollbar(master=self.frame_txt, command=self.txt_widget.yview)
        self.txt_widget['yscrollcommand'] = self.scrollbar_txt.set
        self.scrollbar_txt.pack(side="right", fill="y")
        self.txt_widget.pack(side="bottom", fill="both", expand=True)


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


       
