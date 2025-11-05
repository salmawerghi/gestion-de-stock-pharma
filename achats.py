import tkinter as tk

class AchatsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Module Achats")
        self.window.geometry("900x600")
        self.window.resizable(False, False)

        tk.Label(self.window, text="MODULE ACHATS",
                 font=("Arial", 22, "bold"), fg="white", bg="green").pack(fill='x')

        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Zone de travail ACHATS", 
                 font=("Arial", 14)).pack(pady=20)

        tk.Button(frame, text="Fermer", font=("Arial", 12, "bold"),
                  command=self.window.destroy).pack(pady=20)
