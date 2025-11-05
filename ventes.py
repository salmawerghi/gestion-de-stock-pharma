import tkinter as tk
from tkinter import ttk

class VenteWindow:
    def __init__(self, parent):
        # Créer une nouvelle fenêtre indépendante
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion des Ventes")
        self.window.geometry("900x600")
        self.window.resizable(False, False)

        title = tk.Label(self.window, text="MODULE VENTES",
                         font=("Arial", 22, "bold"), fg="white", bg="#3a38c4")
        title.pack(fill='x')

        # Exemple de contenu
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Zone de travail VENTES", 
                 font=("Arial", 14)).pack(pady=20)

        # Bouton fermer
        tk.Button(frame, text="Fermer", font=("Arial", 12, "bold"),
                  command=self.window.destroy).pack(pady=20)
