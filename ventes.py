import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class VenteWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion des Ventes - Pharmacie")
        self.window.geometry("1250x720")
        self.window.configure(bg="#f0f2f5")
        self.window.resizable(True, True)
        self.cart_items = []

        # >>> correction : ajoute la colonne 'items' si elle n'existe pas <<<
        with sqlite3.connect("pharma_users.db") as conn:
            try:
                conn.execute("ALTER TABLE ventes ADD COLUMN items TEXT;")
                conn.commit()
            except sqlite3.OperationalError:
                pass  # colonne déjà présente : on ignore

        self.create_table()
        self.build_ui()
        self.afficher_ventes()

    # ------------------------------------------------------------------
    #  UI
    # ------------------------------------------------------------------
    def build_ui(self):
        # ───────────── HEADER ─────────────
        tk.Label(self.window, text="GESTION DES VENTES", font=("Arial", 22, "bold"),
                 fg="white", bg="#2c3e50").pack(fill='x')

        # ───────────── CLIENT SECTION ─────────────
        client_frame = tk.LabelFrame(self.window, text="Client", bg="white", fg="#2c3e50", font=("Arial", 11, "bold"))
        client_frame.place(x=20, y=60, width=300, height=150)

        tk.Label(client_frame, text="Nom", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.client_nom = tk.Entry(client_frame, width=25)
        self.client_nom.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(client_frame, text="Prénom", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.client_prenom = tk.Entry(client_frame, width=25)
        self.client_prenom.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(client_frame, text="Contact", bg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.client_contact = tk.Entry(client_frame, width=25)
        self.client_contact.grid(row=2, column=1, padx=10, pady=8)

        # ───────────── PRODUIT SECTION ─────────────
        produit_frame = tk.LabelFrame(self.window, text="Produits", bg="white", fg="#2c3e50", font=("Arial", 11, "bold"))
        produit_frame.place(x=340, y=60, width=400, height=220)

        tk.Label(produit_frame, text="Type Médicament", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.type_med = ttk.Combobox(produit_frame, values=["Comprimé", "Sirop", "Injection", "Pommade", "Gélule"], width=30, state="readonly")
        self.type_med.grid(row=0, column=1, padx=10, pady=8)
        self.type_med.set("Select")

        tk.Label(produit_frame, text="Catégorie", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.categorie = ttk.Combobox(produit_frame, values=["Antibiotique", "Antidouleur", "Vitamine", "Autre"], width=30, state="readonly")
        self.categorie.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(produit_frame, text="Médicament", bg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.medicament = ttk.Combobox(produit_frame, width=30)
        self.medicament.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(produit_frame, text="Prix (TND)", bg="white").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        self.prix = tk.Entry(produit_frame, width=30)
        self.prix.insert(0, "0")
        self.prix.grid(row=3, column=1, padx=10, pady=8)

        tk.Label(produit_frame, text="Quantité", bg="white").grid(row=4, column=0, padx=10, pady=8, sticky="w")
        self.quantite = tk.Entry(produit_frame, width=30)
        self.quantite.insert(0, "0")
        self.quantite.grid(row=4, column=1, padx=10, pady=8)

        # ───────────── BOUTONS SECTION ─────────────
        btn_frame = tk.Frame(self.window, bg="#f0f2f5")
        btn_frame.place(x=340, y=290, width=400, height=150)

        tk.Button(btn_frame, text="Ajouter au Panier", bg="#27ae60", fg="white", width=18, command=self.add_to_cart).grid(row=0, column=0, padx=5, pady=8)
        tk.Button(btn_frame, text="Facturer", bg="#2980b9", fg="white", width=18, command=self.facturer).grid(row=0, column=1, padx=5, pady=8)
        tk.Button(btn_frame, text="Enregistrer Vente", bg="#f39c12", fg="white", width=18, command=self.enregistrer_vente).grid(row=1, column=0, padx=5, pady=8)
        tk.Button(btn_frame, text="Reset", bg="#34495e", fg="white", width=18, command=self.reset_all).grid(row=1, column=1, padx=5, pady=8)

        # ───────────── TOTAUX SECTION ─────────────
        totaux_frame = tk.LabelFrame(self.window, text="TOTAUX", bg="white", fg="#c0392b", font=("Arial", 11, "bold"))
        totaux_frame.place(x=20, y=220, width=300, height=150)

        tk.Label(totaux_frame, text="Total Brut (TND)", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.total_brut = tk.Entry(totaux_frame, width=20, state="readonly")
        self.total_brut.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(totaux_frame, text="TVA 19%", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.tva = tk.Entry(totaux_frame, width=20, state="readonly")
        self.tva.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(totaux_frame, text="Total Net (TND)", bg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.total_net = tk.Entry(totaux_frame, width=20, state="readonly")
        self.total_net.grid(row=2, column=1, padx=10, pady=8)

        # ───────────── FACTURE TABLE ─────────────
        facture_frame = tk.LabelFrame(self.window, text="Facture", bg="white", fg="#2c3e50", font=("Arial", 11, "bold"))
        facture_frame.place(x=760, y=60, width=460, height=380)

        tk.Label(facture_frame, text="Détails Facture", bg="white", font=("Arial", 10, "bold")).pack(pady=5)

        self.facture_tree = ttk.Treeview(facture_frame, columns=("Produit", "Quantité", "Prix"), show="headings", height=13)
        self.facture_tree.heading("Produit", text="Produit")
        self.facture_tree.heading("Quantité", text="Quantité")
        self.facture_tree.heading("Prix", text="Prix")
        self.facture_tree.pack(fill="both", expand=True, padx=5, pady=5)

        total_frame = tk.Frame(facture_frame, bg="white")
        total_frame.pack(fill='x', padx=5, pady=2)
        tk.Label(total_frame, text="TOTAL À PAYER :", bg="white", font=("Arial", 12, "bold"), fg="#c0392b").pack(side='left')
        self.lbl_total_facture = tk.Label(total_frame, text="0.000 TND", bg="white", font=("Arial", 12, "bold"), fg="#c0392b")
        self.lbl_total_facture.pack(side='right')

        # ───────────── HISTORIQUE TABLE ─────────────
        hist_frame = tk.LabelFrame(self.window, text="Historique des Ventes", bg="white", fg="#2c3e50", font=("Arial", 11, "bold"))
        hist_frame.place(x=20, y=380, width=720, height=320)

        columns = ("ref", "client", "date", "total")
        self.tree = ttk.Treeview(hist_frame, columns=columns, show="headings")
        for col, width in zip(columns, [150, 250, 150, 100]):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<ButtonRelease-1>", self.load_facture)

    # ------------------------------------------------------------------
    #  DATABASE
    # ------------------------------------------------------------------
    def create_table(self):
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventes (
                ref TEXT PRIMARY KEY,
                client TEXT,
                date TEXT,
                items TEXT,
                total_brut REAL,
                tva REAL,
                total_net REAL
            )
        ''')
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    #  FUNCTIONS
    # ------------------------------------------------------------------
    def add_to_cart(self):
        med = self.medicament.get()
        qte = self.quantite.get()
        prix = self.prix.get()
        if not med or qte == "0" or prix == "0":
            messagebox.showwarning("Attention", "Remplissez tous les champs produit")
            return
        try:
            self.cart_items.append({
                "produit": med,
                "quantite": float(qte),
                "prix": float(prix)
            })
            messagebox.showinfo("Succès", f"{med} ajouté au panier ✅")
            self.medicament.set("")
            self.quantite.delete(0, tk.END)
            self.quantite.insert(0, "0")
            self.prix.delete(0, tk.END)
            self.prix.insert(0, "0")
        except:
            messagebox.showerror("Erreur", "Valeurs invalides")

    def facturer(self):
        if not self.cart_items:
            messagebox.showwarning("Attention", "Aucun produit dans le panier")
            return
        for item in self.facture_tree.get_children():
            self.facture_tree.delete(item)

        total_brut = sum([item["quantite"] * item["prix"] for item in self.cart_items])
        tva_val = total_brut * 0.19
        total_net_val = total_brut + tva_val

        self.total_brut.config(state="normal")
        self.total_brut.delete(0, tk.END)
        self.total_brut.insert(0, f"{total_brut:.2f}")
        self.total_brut.config(state="readonly")

        self.tva.config(state="normal")
        self.tva.delete(0, tk.END)
        self.tva.insert(0, f"{tva_val:.2f}")
        self.tva.config(state="readonly")

        self.total_net.config(state="normal")
        self.total_net.delete(0, tk.END)
        self.total_net.insert(0, f"{total_net_val:.2f}")
        self.total_net.config(state="readonly")

        self.lbl_total_facture.config(text=f"{total_net_val:.3f} TND")

        for item in self.cart_items:
            subtotal = item["quantite"] * item["prix"]
            self.facture_tree.insert("", tk.END, values=(item["produit"], item["quantite"], f"{subtotal:.2f}"))

    def enregistrer_vente(self):
        if not self.cart_items:
            messagebox.showwarning("Attention", "Aucune facture à enregistrer")
            return
        ref = datetime.now().strftime("%Y%m%d%H%M%S")
        client = f"{self.client_nom.get()} {self.client_prenom.get()}".strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        items_str = str(self.cart_items)
        total_brut = float(self.total_brut.get())
        tva_val = float(self.tva.get())
        total_net = float(self.total_net.get())

        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ventes (ref, client, date, items, total_brut, tva, total_net) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ref, client, date, items_str, total_brut, tva_val, total_net))
        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", "Vente enregistrée ✅")
        self.afficher_ventes()
        self.reset_all()

    def afficher_ventes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ref, client, date, total_net FROM ventes ORDER BY date DESC")
        for ref, client, date, total_net in cursor.fetchall():
            self.tree.insert("", tk.END, values=(ref, client, date, f"{total_net:.3f}"))
        conn.close()

    def reset_all(self):
        self.client_nom.delete(0, tk.END)
        self.client_prenom.delete(0, tk.END)
        self.client_contact.delete(0, tk.END)
        self.medicament.set("")
        self.quantite.delete(0, tk.END)
        self.quantite.insert(0, "0")
        self.prix.delete(0, tk.END)
        self.prix.insert(0, "0")
        self.cart_items = []
        for item in self.facture_tree.get_children():
            self.facture_tree.delete(item)
        for field in [self.total_brut, self.tva, self.total_net]:
            field.config(state="normal")
            field.delete(0, tk.END)
            field.config(state="readonly")
        self.lbl_total_facture.config(text="0.000 TND")

    def load_facture(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        messagebox.showinfo("Info", f"Facture N° {values[0]} sélectionnée")