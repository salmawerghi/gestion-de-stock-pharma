import tkinter as tk
from tkinter import Menu, messagebox
from PIL import Image, ImageTk
import sqlite3
import hashlib
import re

class GestionPharmaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GESTION PHARMACIE")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        self.root.iconbitmap("img1.ico")

        # Création DB
        self.create_database()

        # Page d'accueil
        self.show_auth_page()


    def create_database(self):
        """Crée la base de données SQLite pour les utilisateurs"""
        try:
            conn = sqlite3.connect('pharma_users.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'utilisateur',
                    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute("SELECT * FROM utilisateurs WHERE email = 'admin@pharma.com'")
            if not cursor.fetchone():
                hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO utilisateurs (nom, prenom, email, password, role) VALUES (?, ?, ?, ?, ?)",
                    ("Admin", "System", "admin@pharma.com", hashed_password, "administrateur")
                )

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"❌ Erreur base de données: {e}")


    # ✅ Page accueil = PAS DE FRAME
    def show_auth_page(self):
        """Affiche la page d'authentification directement dans la page principale"""

        # Nettoyer
        for widget in self.root.winfo_children():
            widget.destroy()

        # Image
        try:
            img = Image.open("IMG.png")
            img = img.resize((1200, 700))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            tk.Label(self.root, image=bg).place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        # Titre
        title = tk.Label(self.root, text="GESTION PHARMACIE",
                         font=("Arial", 28, "bold"), bg='#393FB8', fg="white")
        title.pack(pady=(40, 20))

        # Sous-titre


        # Connexion
        tk.Button(self.root, text="SE CONNECTER",
                  font=("Arial", 16, "bold"), bg="#2ecc71", fg="white",
                  width=20, height=2, command=self.show_login_form).place(
              relx=1.0, rely=1.0, anchor='se', x=-600, y=-50
          )

        # Inscription
        tk.Button(self.root, text="S'INSCRIRE",
                  font=("Arial", 16, "bold"), bg="#3498db", fg="white",
                  width=20, height=2, command=self.show_register_form).place(
              relx=1.0, rely=1.0, anchor='se', x=-300, y=-50
          )


    def show_login_form(self):
        """Affiche le formulaire de connexion"""

        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            img = Image.open("IMG.png")
            img = img.resize((1200, 700))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            tk.Label(self.root, image=bg).place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        # Cadre
        login_frame = tk.Frame(self.root, bg='white', relief='raised', bd=3)
        login_frame.place(relx=0.5, rely=0.5, anchor='center', width=450, height=400)

        tk.Label(login_frame, text="CONNEXION",
                 font=("Arial", 20, "bold"), bg='#393FB8', fg='white').pack(fill='x', pady=(0, 30))

        form_frame = tk.Frame(login_frame, bg='white')
        form_frame.pack(pady=20, padx=30, fill='both', expand=True)

        tk.Label(form_frame, text="Email:", bg='white').grid(row=0, column=0, sticky='w', pady=12)
        self.email_entry = tk.Entry(form_frame, width=25, font=("Arial", 12))
        self.email_entry.grid(row=0, column=1, pady=12, padx=15)

        tk.Label(form_frame, text="Mot de passe:", bg='white').grid(row=1, column=0, sticky='w', pady=12)
        self.password_entry = tk.Entry(form_frame, width=25, show='*', font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, pady=12, padx=15)

        btn_frame = tk.Frame(login_frame, bg='white')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Se connecter",
                  font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
                  width=12, command=self.attempt_login).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Retour",
                  font=("Arial", 12), bg="#95a5a6", fg="white",
                  width=12, command=self.show_auth_page).grid(row=0, column=1, padx=10)

        self.email_entry.focus()
        self.root.bind('<Return>', lambda e: self.attempt_login())


    def show_register_form(self):
        """Affiche le formulaire d'inscription"""

        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            img = Image.open("IMG.png")
            img = img.resize((1200, 700))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            tk.Label(self.root, image=bg).place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        register_frame = tk.Frame(self.root, bg='white', relief='raised', bd=3)
        register_frame.place(relx=0.5, rely=0.50, anchor='center', width=500, height=550)

        tk.Label(register_frame, text="INSCRIPTION",
                 font=("Arial", 20, "bold"), bg='#393FB8', fg='white').pack(fill='x', pady=(0, 20))

        form_frame = tk.Frame(register_frame, bg='white')
        form_frame.pack(pady=20, padx=30, fill='both', expand=True)

        tk.Label(form_frame, text="Nom:", bg='white').grid(row=0, column=0, sticky='w', pady=10)
        self.nom_entry = tk.Entry(form_frame, width=25)
        self.nom_entry.grid(row=0, column=1, pady=10, padx=15)

        tk.Label(form_frame, text="Prénom:", bg='white').grid(row=1, column=0, sticky='w', pady=10)
        self.prenom_entry = tk.Entry(form_frame, width=25)
        self.prenom_entry.grid(row=1, column=1, pady=10, padx=15)

        tk.Label(form_frame, text="Email:", bg='white').grid(row=2, column=0, sticky='w', pady=10)
        self.email_reg_entry = tk.Entry(form_frame, width=25)
        self.email_reg_entry.grid(row=2, column=1, pady=10, padx=15)

        tk.Label(form_frame, text="Mot de passe:", bg='white').grid(row=3, column=0, sticky='w', pady=10)
        self.password_reg_entry = tk.Entry(form_frame, width=25, show='*')
        self.password_reg_entry.grid(row=3, column=1, pady=10, padx=15)

        tk.Label(form_frame, text="Confirmer MDP:", bg='white').grid(row=4, column=0, sticky='w', pady=10)
        self.confirm_password_entry = tk.Entry(form_frame, width=25, show='*')
        self.confirm_password_entry.grid(row=4, column=1, pady=10, padx=15)

        btn_frame = tk.Frame(register_frame, bg='white')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="S'inscrire",
                  font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                  width=12, command=self.attempt_register).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Retour",
                  font=("Arial", 12), bg="#95a5a6", fg="white",
                  width=12, command=self.show_auth_page).grid(row=0, column=1, padx=10)

        self.nom_entry.focus()


    # ✅ LOGIN + REGISTER
    def attempt_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if self.authenticate_user(email, password):
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.show_main_app()
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect!")


    def attempt_register(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_reg_entry.get()
        password = self.password_reg_entry.get()
        confirm = self.confirm_password_entry.get()

        if not all([nom, prenom, email, password, confirm]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return

        if password != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas!")
            return

        if not self.is_valid_email(email):
            messagebox.showerror("Erreur", "Email invalide!")
            return

        if self.register_user(nom, prenom, email, password):
            messagebox.showinfo("Succès", "Inscription réussie!")
            self.show_login_form()
        else:
            messagebox.showerror("Erreur", "Email déjà utilisé!")


    def authenticate_user(self, email, password):
        try:
            conn = sqlite3.connect('pharma_users.db')
            cursor = conn.cursor()
            hashed = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute(
                "SELECT * FROM utilisateurs WHERE email = ? AND password = ?",
                (email, hashed)
            )

            user = cursor.fetchone()
            conn.close()

            if user:
                self.current_user = {
                    'id': user[0],
                    'nom': user[1],
                    'prenom': user[2],
                    'email': user[3],
                    'role': user[5]
                }
                return True
            return False

        except:
            return False


    def register_user(self, nom, prenom, email, password):
        try:
            conn = sqlite3.connect('pharma_users.db')
            cursor = conn.cursor()
            hashed = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, password) VALUES (?, ?, ?, ?)",
                (nom, prenom, email, hashed)
            )

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError:
            return False


    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern,email) is not None


    # ✅ PAGE PRINCIPALE
    def show_main_app(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            img = Image.open("IMG.png")
            img = img.resize((1200, 800))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            tk.Label(self.root, image=bg).place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        menu_bar = Menu(self.root)

        fichiers_menu = Menu(menu_bar, tearoff=0)
        fichiers_menu.add_command(label="Nouveau")
        fichiers_menu.add_command(label="Quitter", command=self.root.quit)
        menu_bar.add_cascade(label="Fichiers", menu=fichiers_menu)

        modules_menu = Menu(menu_bar, tearoff=0)
        modules_menu.add_command(label="Achats", command=self.open_achats_window)
        modules_menu.add_command(label="Ventes", command=self.open_ventes_window)
        modules_menu.add_command(label="Listing", command=self.open_listing_window)
        modules_menu.add_command(label="Statistiques", command=self.open_statistiques_window)
        menu_bar.add_cascade(label="Modules", menu=modules_menu)

        self.root.config(menu=menu_bar)

        tk.Label(self.root, text="GESTION DE STOCK PHARMA",
                 font=("Calibri", 32, "bold"), bg="#393FB8", fg="white").place(x=0, y=0, width=1200, height=60)

        tk.Button(self.root, text="Déconnexion",
                  font=("Arial", 12), bg="#3a38c4", fg="white",
                  command=self.show_auth_page).place(relx=0.9, rely=0.9, anchor='center')


    # ✅ Modules :
    def open_ventes_window(self):
        from ventes import VenteWindow
        VenteWindow(self.root)

    def open_achats_window(self):
        from achats import AchatsWindow
        AchatsWindow(self.root)

    def open_listing_window(self):
        from listing import ListingWindow
        ListingWindow(self.root)

    def open_statistiques_window(self):
        from statistiques import StatistiquesWindow
        StatistiquesWindow(self.root)


# Lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = GestionPharmaApp(root)
    root.mainloop()
