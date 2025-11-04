import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk

# ─────────────────────────────────────────────
# ✅ Fenêtre principale
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("GESTION PHARMACIE")
root.geometry("1200x700")
root.resizable(False, False)

# ─────────────────────────────────────────────
# ✅ IMAGE BACKGROUND
# ─────────────────────────────────────────────
# Remplace cette image par ton fichier local
img_path = "IMG.png"      # <---- A MODIFIER
img = Image.open(img_path)
img = img.resize((1200, 800))
bg = ImageTk.PhotoImage(img)

bg_label = tk.Label(root, image=bg)
bg_label.place(x=0, y=0)

# ─────────────────────────────────────────────
# ✅ BARRE DE MENU
# ─────────────────────────────────────────────
menu_bar = Menu(root)

# ---- FICHIERS
fichiers_menu = Menu(menu_bar, tearoff=0)
fichiers_menu.add_command(label="Nouveau")
fichiers_menu.add_command(label="Quitter", command=root.quit)
menu_bar.add_cascade(label="Fichiers", menu=fichiers_menu)

# ---- MODULES
modules_menu = Menu(menu_bar, tearoff=0)
modules_menu.add_command(label="Achats")
modules_menu.add_command(label="Ventes")
modules_menu.add_command(label="Listing")
modules_menu.add_command(label="Factures")
menu_bar.add_cascade(label="Modules", menu=modules_menu)

# ---- A PROPOS
apropos_menu = Menu(menu_bar, tearoff=0)
apropos_menu.add_command(label="A propos du système")
menu_bar.add_cascade(label="A propos", menu=apropos_menu)

# ---- AIDE
aide_menu = Menu(menu_bar, tearoff=0)
aide_menu.add_command(label="Aide")
menu_bar.add_cascade(label="Aide?", menu=aide_menu)

root.config(menu=menu_bar)

# ─────────────────────────────────────────────
# ✅ TITRE HAUT
# ─────────────────────────────────────────────
title = tk.Label(root, text="GESTION DE STOCK PHARMA",
                font=("Calibri", 32, "bold italic"), bg="#393FB8", fg="white")
title.place(x=0, y=0, width=1200, height=60)

# ─────────────────────────────────────────────
# ✅ LANCEMENT
# ─────────────────────────────────────────────
root.mainloop()
