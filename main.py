import tkinter as tk
from serena_assistant import SerenaAssistant

def main():
    root = tk.Tk()
    app = SerenaAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()