import tkinter as tk

class FindWordsAppClass(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_main_window()
        self.create_text_widgets()
        self.create_ok_and_exit_btns()

    def create_main_window(self) -> None:
        self.master.title("Find Words")
        self.master.geometry("800x700")

    def create_text_widgets(self) -> None:
        self.ent_text = tk.Entry()
        self.ent_text.pack()
        self.txt_widget = tk.Text()
        self.txt_widget.pack()

    def create_ok_and_exit_btns(self) -> None:
        frame_btn = tk.Frame(self.master)
        frame_btn.pack(side="bottom", fill="y", expand=True)
        frame_btn_ok = tk.Frame(master=frame_btn)
        frame_btn_ok.pack(side="left", fill="both", expand=True,  padx=10, pady=10)
        frame_btn_exit = tk.Frame(master=frame_btn)
        frame_btn_exit.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.btn_ok = tk.Button(master=frame_btn_ok, width=10)
        self.btn_ok["text"] = "OK"
        #self.ok_button["command"] = self.com
        self.btn_ok.pack()

        self.btn_exit = tk.Button(master=frame_btn_exit, width=10)
        self.btn_exit["text"] = "Exit"
        #self.btn_exit["command"] = self.com
        self.btn_exit.pack()


       
