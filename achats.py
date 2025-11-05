import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk


class AchatsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Achat Médicament - Gestion Pharmacie")
        self.window.geometry("1200x700")
        self.window.resizable(False, False)
        self.window.configure(bg="#f4f6f9")
        self.window.iconbitmap("img1.ico")

        # ─────────────────────────────
        # DATABASE
        # ─────────────────────────────
        self.create_table()

        # HEADER
        tk.Label(self.window, text="ACHAT MÉDICAMENT",
                 font=("Arial", 22, "bold"), bg="#2980b9", fg="white").pack(fill="x")

        # ─────────────────────────────
        # FORM FRAME (with background image)
        # ─────────────────────────────
        form_frame = tk.LabelFrame(self.window, text="Informations sur le Médicament",
                                   bg="white", font=("Arial", 12, "bold"), fg="#2980b9")
        form_frame.place(x=20, y=60, width=1160, height=200)

        # ✅ Background inside the fieldset
        try:
            form_bg = Image.open("info_background.jpg")  # your image file
            form_bg = form_bg.resize((1160, 200))
            self.form_bg_photo = ImageTk.PhotoImage(form_bg)
            bg_label_form = tk.Label(form_frame, image=self.form_bg_photo, bg="white")
            bg_label_form.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"⚠️ Erreur chargement image form : {e}")

        # Form labels and entries
        labels = [
            "N° Référence :", "Nom Company :", "Type Médicament :", "Nom Médicament :",
            "Date Fab :", "Date Exp :", "Prix Plaquette :", "Quantité :"
        ]

        self.ref_entry = tk.Entry(form_frame, width=20)
        self.company_entry = tk.Entry(form_frame, width=20)
        self.type_entry = tk.Entry(form_frame, width=20)
        self.nom_med_entry = tk.Entry(form_frame, width=20)
        self.date_fab_entry = tk.Entry(form_frame, width=20)
        self.date_exp_entry = tk.Entry(form_frame, width=20)
        self.prix_entry = tk.Entry(form_frame, width=20)
        self.qte_entry = tk.Entry(form_frame, width=20)
        entries = [self.ref_entry, self.company_entry, self.type_entry, self.nom_med_entry,
                   self.date_fab_entry, self.date_exp_entry, self.prix_entry, self.qte_entry]

        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg="white", font=("Arial", 11)).grid(
                row=i // 4, column=(i % 4) * 2, padx=10, pady=8, sticky="w"
            )
            entries[i].grid(row=i // 4, column=(i % 4) * 2 + 1, padx=10, pady=8)

        # ─────────────────────────────
        # BUTTON FRAME
        # ─────────────────────────────
        btn_frame = tk.Frame(self.window, bg="#f4f6f9")
        btn_frame.place(x=20, y=270, width=1160, height=50)

        tk.Button(btn_frame, text="Ajouter", bg="#2980b9", fg="white", font=("Arial", 11, "bold"),
                  width=15, command=self.ajouter_medicament).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Modifier", bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                  width=15, command=self.modifier_medicament).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Supprimer", bg="#c0392b", fg="white", font=("Arial", 11, "bold"),
                  width=15, command=self.supprimer_medicament).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Reset", bg="#7f8c8d", fg="white", font=("Arial", 11, "bold"),
                  width=15, command=self.clear_fields).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Fermer", bg="#34495e", fg="white", font=("Arial", 11, "bold"),
                  width=15, command=self.window.destroy).pack(side="right", padx=10)

        # ─────────────────────────────
        # SEARCH BAR
        # ─────────────────────────────
        search_frame = tk.Frame(self.window, bg="#f4f6f9")
        search_frame.place(x=20, y=330, width=1160, height=40)

        tk.Label(search_frame, text="Rechercher par :", font=("Arial", 11, "bold"),
                 bg="#f4f6f9").pack(side="left", padx=10)

        self.search_var = tk.StringVar()
        self.search_box = ttk.Combobox(search_frame, textvariable=self.search_var, width=20, state="readonly")
        self.search_box["values"] = ("Référence", "Nom Médicament", "Company")
        self.search_box.current(0)
        self.search_box.pack(side="left", padx=10)

        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)

        tk.Button(search_frame, text="Search", bg="#2980b9", fg="white", font=("Arial", 11, "bold"),
                  command=self.search_medicament).pack(side="left", padx=10)
        tk.Button(search_frame, text="Tout", bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                  command=self.afficher_medicaments).pack(side="left", padx=10)

        # ─────────────────────────────
        # TABLE FRAME
        # ─────────────────────────────
        table_frame = tk.Frame(self.window, bg="white", bd=2, relief="groove")
        table_frame.place(x=20, y=380, width=1160, height=300)

        columns = ("ref", "company", "type", "nom", "fab", "exp", "prix", "qte")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        headings = ["Réf", "Company", "Type Médicament", "Nom Médicament",
                    "Date Fab", "Date Exp", "Prix Plaquette", "Quantité"]

        for col, head in zip(columns, headings):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=130, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.selectionner_ligne)

        self.afficher_medicaments()

    # ─────────────────────────────
    # DATABASE FUNCTIONS
    # ─────────────────────────────
    def create_table(self):
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicaments (
                ref TEXT PRIMARY KEY,
                company TEXT,
                type TEXT,
                nom TEXT,
                date_fab TEXT,
                date_exp TEXT,
                prix REAL,
                quantite INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def ajouter_medicament(self):
        data = (
            self.ref_entry.get(), self.company_entry.get(), self.type_entry.get(),
            self.nom_med_entry.get(), self.date_fab_entry.get(), self.date_exp_entry.get(),
            self.prix_entry.get(), self.qte_entry.get()
        )

        if not all(data):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires !")
            return

        try:
            conn = sqlite3.connect("pharma_users.db")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO medicaments VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Médicament ajouté avec succès ✅")
            self.afficher_medicaments()
            self.clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Référence déjà existante !")

    def afficher_medicaments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicaments ORDER BY date_exp ASC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def supprimer_medicament(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Sélectionnez un médicament à supprimer.")
            return
        ref = self.tree.item(selected[0], "values")[0]
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medicaments WHERE ref = ?", (ref,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Médicament supprimé 🗑️")
        self.afficher_medicaments()

    def modifier_medicament(self):
        data = (
            self.company_entry.get(), self.type_entry.get(), self.nom_med_entry.get(),
            self.date_fab_entry.get(), self.date_exp_entry.get(),
            self.prix_entry.get(), self.qte_entry.get(), self.ref_entry.get()
        )
        if not all(data):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires !")
            return

        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE medicaments
            SET company=?, type=?, nom=?, date_fab=?, date_exp=?, prix=?, quantite=?
            WHERE ref=?
        ''', data)
        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Médicament modifié avec succès ✏️")
        self.afficher_medicaments()
        self.clear_fields()

    def search_medicament(self):
        critere = self.search_box.get()
        valeur = self.search_entry.get().strip()
        if not valeur:
            messagebox.showwarning("Avertissement", "Entrez une valeur de recherche.")
            return

        mapping = {"Référence": "ref", "Nom Médicament": "nom", "Company": "company"}
        colonne = mapping[critere]

        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM medicaments WHERE {colonne} LIKE ?", ('%' + valeur + '%',))
        rows = cursor.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_fields(self):
        for entry in [self.ref_entry, self.company_entry, self.type_entry, self.nom_med_entry,
                      self.date_fab_entry, self.date_exp_entry, self.prix_entry, self.qte_entry]:
            entry.delete(0, tk.END)

    def selectionner_ligne(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")

        entries = [self.ref_entry, self.company_entry, self.type_entry, self.nom_med_entry,
                   self.date_fab_entry, self.date_exp_entry, self.prix_entry, self.qte_entry]

        for entry in entries:
            entry.delete(0, tk.END)
        for i, value in enumerate(values):
            entries[i].insert(0, value)
