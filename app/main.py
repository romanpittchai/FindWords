import tkinter as tk
from gui import FindWordsAppClass

if __name__ == "__main__":
    root = tk.Tk()
    app = FindWordsAppClass(master=root)
    app.mainloop()