import tkinter as tk
from gui import FindWordsAppClass
from ttkthemes import ThemedTk

def main() -> None:
    root = ThemedTk(theme="adapta") #breeze
    app = FindWordsAppClass(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()