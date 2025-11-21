import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
from datetime import datetime
from PIL import Image, ImageTk


class VenteWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion des Ventes - Pharmacie")
        self.window.geometry("1250x720")
        self.window.configure(bg="#f0f2f5")
        self.window.resizable(False, False)
        self.cart_items = []

        with sqlite3.connect("pharma_users.db") as conn:
            try:
                conn.execute("ALTER TABLE ventes ADD COLUMN items TEXT;")
                conn.commit()
            except:
                pass

        self.create_table()
        self.types = self.get_types()
        self.build_ui()
        self.afficher_ventes()

    # ------------------------------------------------------------
    # DATABASE
    # ------------------------------------------------------------
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

    def get_types(self):
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT type FROM medicaments")
        types = [row[0] for row in cursor.fetchall()]
        conn.close()
        return types

    # ------------------------------------------------------------
    # UI
    # ------------------------------------------------------------
    def build_ui(self):
        tk.Label(self.window, text="GESTION DES VENTES", font=("Arial", 22, "bold"),
                 fg="white", bg="#2c3e50").pack(fill='x')

        # ───────── SECTION CLIENT ─────────
        client_frame = tk.LabelFrame(self.window, text="Client", bg="white", fg="#2c3e50", highlightbackground="#324A8A", highlightthickness=3,
                                     font=("Arial", 11, "bold"))
        client_frame.place(x=20, y=60, width=300, height=150)

        tk.Label(client_frame, text="Nom", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.client_nom = tk.Entry(client_frame, width=25)
        self.client_nom.grid(row=0, column=1)

        tk.Label(client_frame, text="Prénom", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.client_prenom = tk.Entry(client_frame, width=25)
        self.client_prenom.grid(row=1, column=1)

        tk.Label(client_frame, text="Contact", bg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.client_contact = tk.Entry(client_frame, width=25)
        self.client_contact.grid(row=2, column=1)

        # ───────── SECTION PRODUITS ─────────
        produit_frame = tk.LabelFrame(self.window, highlightbackground="#324A8A", highlightthickness=3, text="Produits", bg="white", fg="#2c3e50", font=("Arial", 11, "bold"))
        produit_frame.place(x=340, y=60, width=400, height=220)

        tk.Label(produit_frame, text="Type Médicament", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.type_med = ttk.Combobox(produit_frame, values=self.types, width=30, state="readonly")
        self.type_med.bind("<<ComboboxSelected>>", self.update_medicaments)
        self.type_med.grid(row=0, column=1, padx=10, pady=8)
        self.type_med.set("Select")

        tk.Label(produit_frame, text="Médicament", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.medicament = ttk.Combobox(produit_frame, width=30)
        self.medicament.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(produit_frame, text="Prix (TND)", bg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.prix = tk.Entry(produit_frame, width=30)
        self.prix.insert(0, "0")
        self.prix.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(produit_frame, text="Quantité", bg="white").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        self.quantite = tk.Entry(produit_frame, width=30)
        self.quantite.insert(0, "0")
        self.quantite.grid(row=3, column=1, padx=10, pady=8)

        # ───────── BOUTONS ─────────
        btn_frame = tk.Frame(self.window, bg="#f0f2f5")
        btn_frame.place(x=340, y=290, width=400, height=150)

        tk.Button(btn_frame, text="Ajouter au Panier", bg="#27ae60", fg="white",
                  width=18, command=self.add_to_cart).grid(row=0, column=0, padx=5, pady=8)

        tk.Button(btn_frame, text="Facturer", bg="#2980b9", fg="white",
                  width=18, command=self.facturer).grid(row=0, column=1, padx=5, pady=8)

        tk.Button(btn_frame, text="Enregistrer", bg="#f39c12", fg="white",
                  width=18, command=self.enregistrer_vente).grid(row=1, column=0, padx=5, pady=8)

        tk.Button(btn_frame, text="Reset", bg="#34495e", fg="white",
                  width=18, command=self.reset_all).grid(row=1, column=1, padx=5, pady=8)

        # ───────── TOTALS ─────────
        totaux_frame = tk.LabelFrame(self.window, text="TOTAUX", bg="white", fg="#c0392b", highlightbackground="#324A8A", highlightthickness=3,
                                     font=("Arial", 11, "bold"))
        totaux_frame.place(x=20, y=220, width=300, height=150)

        tk.Label(totaux_frame, text="Total Brut", bg="white").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.total_brut = tk.Entry(totaux_frame, width=15, state="readonly")
        self.total_brut.grid(row=0, column=1)

        tk.Label(totaux_frame, text="TVA 19%", bg="white").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.tva = tk.Entry(totaux_frame, width=15, state="readonly")
        self.tva.grid(row=1, column=1)

        tk.Label(totaux_frame, text="Total Net", bg="white").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.total_net = tk.Entry(totaux_frame, width=15, state="readonly")
        self.total_net.grid(row=2, column=1)

        # ───────── FACTURE (VISUEL STYLE IMAGE) ─────────
        facture_frame = tk.Frame(self.window, bg="white", highlightbackground="#324A8A", highlightthickness=3)
        facture_frame.place(x=760, y=60, width=460, height=640)

        tk.Label(facture_frame, text="Facture", font=("Arial", 18, "bold"),
                 fg="#2c3e50", bg="white").pack(pady=5)

        tk.Label(facture_frame, text=".........................................................",
                 bg="white").pack()

        infos_frame = tk.Frame(facture_frame, bg="white")
        infos_frame.pack(anchor="w", padx=10, pady=5)

        tk.Label(infos_frame, text="N° Facture :", bg="white").grid(row=0, column=0, sticky="w")
        self.facture_num_label = tk.Label(infos_frame, text="", bg="white")
        self.facture_num_label.grid(row=0, column=1, sticky="w")

        tk.Label(infos_frame, text="Nom :", bg="white").grid(row=1, column=0, sticky="w")
        self.facture_nom_label = tk.Label(infos_frame, text="", bg="white")
        self.facture_nom_label.grid(row=1, column=1, sticky="w")

        tk.Label(infos_frame, text="Prénom :", bg="white").grid(row=2, column=0, sticky="w")
        self.facture_prenom_label = tk.Label(infos_frame, text="", bg="white")
        self.facture_prenom_label.grid(row=2, column=1, sticky="w")

        tk.Label(infos_frame, text="Contact :", bg="white").grid(row=3, column=0, sticky="w")
        self.facture_contact_label = tk.Label(infos_frame, text="", bg="white")
        self.facture_contact_label.grid(row=3, column=1, sticky="w")

        tk.Label(facture_frame, text="=" * 65, bg="white").pack()

        self.facture_tree = ttk.Treeview(facture_frame, columns=("Produit", "Quantité", "Prix"),
                                         show="headings", height=9)
        self.facture_tree.heading("Produit", text="PRODUIT")
        self.facture_tree.heading("Quantité", text="QUANTITE")
        self.facture_tree.heading("Prix", text="PRIX")
        self.facture_tree.pack(fill="both", padx=5, pady=5)

        total_frame = tk.Frame(facture_frame, bg="white")
        total_frame.pack(fill='x', padx=5, pady=8)
        tk.Label(total_frame, text="TOTAL À PAYER :", bg="white",
                 font=("Arial", 14, "bold"), fg="red").pack(side='left')
        self.lbl_total_facture = tk.Label(total_frame, text="0.000 TND", bg="white",
                                          font=("Arial", 14, "bold"), fg="red")
        self.lbl_total_facture.pack(side='right')

        # ───────── IMAGE À DROITE ─────────
        try:
            img = Image.open("IMG.png")
            img = img.resize((460, 200))
            self.photo = ImageTk.PhotoImage(img)
            tk.Label(facture_frame, image=self.photo, bg="white").pack()
        except:
            tk.Label(facture_frame, text="[ IMAGE ]", bg="white").pack()

        # ───────── HISTORIQUE ─────────
        hist_frame = tk.LabelFrame(self.window, text="Historique des Ventes", bg="white", highlightbackground="#324A8A", highlightthickness=3,
                                   fg="#2c3e50", font=("Arial", 11, "bold"))
        hist_frame.place(x=20, y=380, width=720, height=320)

        columns = ("ref", "client", "date", "total")
        self.tree = ttk.Treeview(hist_frame, columns=columns, show="headings")
        for col, width in zip(columns, [150, 250, 160, 100]):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)


    # ------------------------------------------------------------
    # FUNCTIONS
    # ------------------------------------------------------------
    def add_to_cart(self):
        med = self.medicament.get()  # Get selected medication
        qte = self.quantite.get()    # Get the quantity to be purchased
        prix = self.prix.get()       # Get the price of the medication

        if not med or qte == "0" or prix == "0":
            messagebox.showwarning("Attention", "Remplissez tous les champs")
            return

        try:
            # Convert quantity to integer and price to float
            quantity = int(qte)
            price = float(prix)

            # Fetch the current stock quantity of the selected medication
            conn = sqlite3.connect("pharma_users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT quantite FROM medicaments WHERE nom=?", (med,))
            result = cursor.fetchone()
            if result:
                current_quantity = result[0]

                # Check if enough stock is available
                if quantity > current_quantity:
                    messagebox.showwarning("Attention", "Quantité demandée supérieure à la stock disponible.")
                    conn.close()
                    return

                # Add the medication to the cart
                self.cart_items.append({
                    "produit": med,
                    "quantite": quantity,
                    "prix": price
                })

                # Decrease the quantity in the database
                new_quantity = current_quantity - quantity
                cursor.execute("UPDATE medicaments SET quantite=? WHERE nom=?", (new_quantity, med))
                conn.commit()

                messagebox.showinfo("Succès", f"{med} ajouté au panier ✅")

                # Optionally update the "Médicament" combobox to reflect the updated stock
                self.update_medicaments(None)  # Refresh the medication list to reflect the stock change

            else:
                messagebox.showwarning("Erreur", "Médicament non trouvé.")

            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'ajout au panier: {e}")

    def facturer(self):
        if not self.cart_items:
            messagebox.showwarning("Attention", "Panier vide")
            return

        for item in self.facture_tree.get_children():
            self.facture_tree.delete(item)

        total_brut = sum([item["quantite"] * item["prix"] for item in self.cart_items])
        tva_val = total_brut * 0.19
        total_net_val = total_brut + tva_val

        self.total_brut.config(state="normal")
        self.tva.config(state="normal")
        self.total_net.config(state="normal")

        self.total_brut.delete(0, tk.END)
        self.tva.delete(0, tk.END)
        self.total_net.delete(0, tk.END)

        self.total_brut.insert(0, f"{total_brut:.3f}")
        self.tva.insert(0, f"{tva_val:.3f}")
        self.total_net.insert(0, f"{total_net_val:.3f}")

        self.total_brut.config(state="readonly")
        self.tva.config(state="readonly")
        self.total_net.config(state="readonly")

        self.lbl_total_facture.config(text=f"{total_net_val:.3f} TND")

        # REMPLY INFO FACTURE
        self.facture_nom_label.config(text=self.client_nom.get())
        self.facture_prenom_label.config(text=self.client_prenom.get())
        self.facture_contact_label.config(text=self.client_contact.get())
        self.facture_num_label.config(text=datetime.now().strftime("%Y%m%d%H%M%S"))

        for item in self.cart_items:
            subtotal = item["quantite"] * item["prix"]
            self.facture_tree.insert("", tk.END,
                                     values=(item["produit"], item["quantite"], f"{subtotal:.2f}"))
    
    def enregistrer_vente(self):
        if not self.cart_items:
            messagebox.showwarning("Attention", "Aucune vente")
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

    # Update the medications based on the selected type
    def update_medicaments(self, event=None):
        # Get the selected type of medication from the combo box
        med_type = self.type_med.get()

        # Fetch medications based on the selected type from the database using Pandas
        conn = sqlite3.connect("pharma_users.db")
        query = f"SELECT nom FROM medicaments WHERE type='{med_type}'"
        medicaments_df = pd.read_sql_query(query, conn)
        conn.close()

        # Update the "Médicament" combobox with the filtered medications
        self.medicament['values'] = medicaments_df['nom'].tolist()
        self.medicament.set("")  # Reset the selection

        # Update the "Médicament" combobox when a selection is made
        self.medicament.bind("<<ComboboxSelected>>", self.update_price)

    def update_price(self, event):
        # Get the selected medication from the combobox
        selected_med = self.medicament.get()

        # Fetch the price of the selected medication from the database
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT prix FROM medicaments WHERE nom=?", (selected_med,))
        result = cursor.fetchone()
        conn.close()

        if result:
            # Update the "Prix" field with the price of the selected medication
            self.prix.delete(0, tk.END)
            self.prix.insert(0, str(result[0]))
