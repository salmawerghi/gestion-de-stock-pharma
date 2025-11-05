import tkinter as tk

class ListingWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Module Listing - Gestion Pharmacie")
        self.window.geometry("600x400")
        self.window.configure(bg="#f4f4f4")

        tk.Label(self.window, text="Page Listing",
                 font=("Arial", 20, "bold"), bg="#393FB8", fg="white").pack(fill='x', pady=10)

        tk.Label(self.window, text="Ici s'affichera la liste des produits / stocks.",
                 font=("Arial", 12), bg="#f4f4f4").pack(pady=40)

        tk.Button(self.window, text="Fermer", bg="#e74c3c", fg="white",
                  font=("Arial", 12), command=self.window.destroy).pack(pady=20)