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
        
        # Créer la base de données
        self.create_database()
        
        # Afficher la page d'authentification (connexion/inscription)
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
            print("✅ Base de données créée avec succès!")
            
        except sqlite3.Error as e:
            print(f"❌ Erreur base de données: {e}")

    def show_auth_page(self):
        """Affiche la page d'authentification (choix connexion/inscription)"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Image de fond
        try:
            img_path = "IMG.png"
            img = Image.open(img_path)
            img = img.resize((1200, 700))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            bg_label = tk.Label(self.root, image=bg)
            bg_label.place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        # Cadre principal d'authentification
        auth_frame = tk.Frame(self.root, bg='white', relief='raised', bd=3)
        auth_frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=400)

        # Titre
        title_label = tk.Label(auth_frame, text="GESTION PHARMACIE", 
                              font=("Arial", 24, "bold"), bg='#393FB8', fg='white')
        title_label.pack(fill='x', pady=(0, 30))

        # Sous-titre
        subtitle_label = tk.Label(auth_frame, text="Choisissez une option", 
                                 font=("Arial", 14), bg='white', fg='#2c3e50')
        subtitle_label.pack(pady=(0, 30))

        # Bouton Connexion
        login_btn = tk.Button(auth_frame, text="SE CONNECTER", 
                             font=("Arial", 14, "bold"), bg="#2ecc71", fg="white",
                             width=20, height=2, command=self.show_login_form)
        login_btn.pack(pady=15)

        # Bouton Inscription
        register_btn = tk.Button(auth_frame, text="S'INSCRIRE", 
                               font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                               width=20, height=2, command=self.show_register_form)
        register_btn.pack(pady=15)

    def show_login_form(self):
        """Affiche le formulaire de connexion"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Image de fond
        try:
            img_path = "IMG.png"
            img = Image.open(img_path)
            img = img.resize((1200, 700))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            bg_label = tk.Label(self.root, image=bg)
            bg_label.place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        # Cadre de connexion
        login_frame = tk.Frame(self.root, bg='white', relief='raised', bd=3)
        login_frame.place(relx=0.5, rely=0.5, anchor='center', width=450, height=400)

        # Titre
        title_label = tk.Label(login_frame, text="CONNEXION", 
                              font=("Arial", 20, "bold"), bg='#393FB8', fg='white')
        title_label.pack(fill='x', pady=(0, 30))

        # Formulaire
        form_frame = tk.Frame(login_frame, bg='white')
        form_frame.pack(pady=20, padx=30, fill='both', expand=True)

        # Email
        tk.Label(form_frame, text="Email:", bg='white', 
                font=("Arial", 12)).grid(row=0, column=0, sticky='w', pady=12)
        self.email_entry = tk.Entry(form_frame, width=25, font=("Arial", 12))
        self.email_entry.grid(row=0, column=1, pady=12, padx=15)

        # Mot de passe
        tk.Label(form_frame, text="Mot de passe:", bg='white',
                font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=12)
        self.password_entry = tk.Entry(form_frame, width=25, show='*', font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, pady=12, padx=15)

        # Boutons
        btn_frame = tk.Frame(login_frame, bg='white')
        btn_frame.pack(pady=20)

        # Bouton Connexion
        login_btn = tk.Button(btn_frame, text="Se connecter",
                             font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
                             width=12, command=self.attempt_login)
        login_btn.grid(row=0, column=0, padx=10)

        # Bouton Retour
        back_btn = tk.Button(btn_frame, text="Retour",
                           font=("Arial", 12), bg="#95a5a6", fg="white",
                           width=12, command=self.show_auth_page)
        back_btn.grid(row=0, column=1, padx=10)

        # Lien vers inscription
        register_link = tk.Label(login_frame, text="Créer un compte", 
                                font=("Arial", 10), bg='white', fg='#3498db',
                                cursor="hand2")
        register_link.pack(pady=10)
        register_link.bind("<Button-1>", lambda e: self.show_register_form())

        # Focus et raccourci Entrée
        self.email_entry.focus()
        self.root.bind('<Return>', lambda e: self.attempt_login())

    def show_register_form(self):
        """Affiche le formulaire d'inscription"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Image de fond
        try:
            img_path = "IMG.png"
            img = Image.open(img_path)
            img = img.resize((1200, 700))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            bg_label = tk.Label(self.root, image=bg)
            bg_label.place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        # Cadre d'inscription
        register_frame = tk.Frame(self.root, bg='white', relief='raised', bd=3)
        register_frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=550)

        # Titre
        title_label = tk.Label(register_frame, text="INSCRIPTION", 
                              font=("Arial", 20, "bold"), bg='#393FB8', fg='white')
        title_label.pack(fill='x', pady=(0, 20))

        # Formulaire
        form_frame = tk.Frame(register_frame, bg='white')
        form_frame.pack(pady=20, padx=30, fill='both', expand=True)

        # Nom
        tk.Label(form_frame, text="Nom:", bg='white', 
                font=("Arial", 12)).grid(row=0, column=0, sticky='w', pady=10)
        self.nom_entry = tk.Entry(form_frame, width=25, font=("Arial", 12))
        self.nom_entry.grid(row=0, column=1, pady=10, padx=15)

        # Prénom
        tk.Label(form_frame, text="Prénom:", bg='white',
                font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=10)
        self.prenom_entry = tk.Entry(form_frame, width=25, font=("Arial", 12))
        self.prenom_entry.grid(row=1, column=1, pady=10, padx=15)

        # Email
        tk.Label(form_frame, text="Email:", bg='white',
                font=("Arial", 12)).grid(row=2, column=0, sticky='w', pady=10)
        self.email_reg_entry = tk.Entry(form_frame, width=25, font=("Arial", 12))
        self.email_reg_entry.grid(row=2, column=1, pady=10, padx=15)

        # Mot de passe
        tk.Label(form_frame, text="Mot de passe:", bg='white',
                font=("Arial", 12)).grid(row=3, column=0, sticky='w', pady=10)
        self.password_reg_entry = tk.Entry(form_frame, width=25, show='*', font=("Arial", 12))
        self.password_reg_entry.grid(row=3, column=1, pady=10, padx=15)

        # Confirmation mot de passe
        tk.Label(form_frame, text="Confirmer MDP:", bg='white',
                font=("Arial", 12)).grid(row=4, column=0, sticky='w', pady=10)
        self.confirm_password_entry = tk.Entry(form_frame, width=25, show='*', font=("Arial", 12))
        self.confirm_password_entry.grid(row=4, column=1, pady=10, padx=15)

        # Boutons
        btn_frame = tk.Frame(register_frame, bg='white')
        btn_frame.pack(pady=20)

        # Bouton Inscription
        register_btn = tk.Button(btn_frame, text="S'inscrire",
                               font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                               width=12, command=self.attempt_register)
        register_btn.grid(row=0, column=0, padx=10)

        # Bouton Retour
        back_btn = tk.Button(btn_frame, text="Retour",
                           font=("Arial", 12), bg="#95a5a6", fg="white",
                           width=12, command=self.show_auth_page)
        back_btn.grid(row=0, column=1, padx=10)

        # Lien vers connexion
        login_link = tk.Label(register_frame, text="Déjà un compte? Se connecter", 
                             font=("Arial", 10), bg='white', fg='#27ae60',
                             cursor="hand2")
        login_link.pack(pady=10)
        login_link.bind("<Button-1>", lambda e: self.show_login_form())

        # Focus
        self.nom_entry.focus()

    def attempt_login(self):
        """Tente de connecter l'utilisateur"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if self.authenticate_user(email, password):
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.show_main_app()
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect!")

    def attempt_register(self):
        """Tente d'inscrire un nouvel utilisateur"""
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_reg_entry.get()
        password = self.password_reg_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([nom, prenom, email, password, confirm_password]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return

        if password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas!")
            return

        if not self.is_valid_email(email):
            messagebox.showerror("Erreur", "Format d'email invalide!")
            return

        if self.register_user(nom, prenom, email, password):
            messagebox.showinfo("Succès", "Inscription réussie! Veuillez vous connecter.")
            self.show_login_form()
        else:
            messagebox.showerror("Erreur", "Cet email est déjà utilisé!")

    def authenticate_user(self, email, password):
        """Authentifie l'utilisateur"""
        try:
            conn = sqlite3.connect('pharma_users.db')
            cursor = conn.cursor()
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute(
                "SELECT * FROM utilisateurs WHERE email = ? AND password = ?",
                (email, hashed_password)
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
            
        except sqlite3.Error:
            return False

    def register_user(self, nom, prenom, email, password):
        """Inscrit un nouvel utilisateur"""
        try:
            conn = sqlite3.connect('pharma_users.db')
            cursor = conn.cursor()
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, password) VALUES (?, ?, ?, ?)",
                (nom, prenom, email, hashed_password)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            return False

    def is_valid_email(self, email):
        """Valide le format de l'email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def show_main_app(self):
        """Affiche l'application principale après connexion réussie"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Image de fond
        try:
            img_path = "IMG.png"
            img = Image.open(img_path)
            img = img.resize((1200, 800))
            bg = ImageTk.PhotoImage(img)
            self.bg_image = bg
            bg_label = tk.Label(self.root, image=bg)
            bg_label.place(x=0, y=0)
        except:
            self.root.configure(bg='#f4f4f4')

        # Barre de menu
        menu_bar = Menu(self.root)
        
        # Menu Fichiers
        fichiers_menu = Menu(menu_bar, tearoff=0)
        fichiers_menu.add_command(label="Nouveau")
        fichiers_menu.add_command(label="Quitter", command=self.root.quit)
        menu_bar.add_cascade(label="Fichiers", menu=fichiers_menu)

        # Menu Modules
        modules_menu = Menu(menu_bar, tearoff=0)
        modules_menu.add_command(label="Achats")
        modules_menu.add_command(label="Ventes")
        modules_menu.add_command(label="Listing")
        modules_menu.add_command(label="Factures")
        menu_bar.add_cascade(label="Modules", menu=modules_menu)

        # Autres menus
        apropos_menu = Menu(menu_bar, tearoff=0)
        apropos_menu.add_command(label="A propos du système")
        menu_bar.add_cascade(label="A propos", menu=apropos_menu)

        aide_menu = Menu(menu_bar, tearoff=0)
        aide_menu.add_command(label="Aide")
        menu_bar.add_cascade(label="Aide?", menu=aide_menu)

        self.root.config(menu=menu_bar)

        # Titre principal
        title = tk.Label(self.root, text="GESTION DE STOCK PHARMA",
                        font=("Calibri", 32, "bold italic"), bg="#393FB8", fg="white")
        title.place(x=0, y=0, width=1200, height=60)


        # Bouton Déconnexion
        logout_btn = tk.Button(self.root, text="Déconnexion",
                             font=("Arial", 12), bg="#3a38c4", fg="white",
                             command=self.show_auth_page)
        logout_btn.place(relx=0.9, rely=0.9, anchor='center')

# ─────────────────────────────────────────────
# ✅ LANCEMENT DE L'APPLICATION
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = GestionPharmaApp(root)
    root.mainloop()