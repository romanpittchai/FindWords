import tkinter as tk
from gui import FindWordsAppClass
from ttkthemes import ThemedTk
import platform
from constants import CHECK_OS, THEMES_APP


def main() -> None:    
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