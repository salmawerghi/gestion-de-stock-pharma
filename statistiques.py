import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class StatistiquesWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Module Statistiques - Gestion Pharmacie")
        self.window.geometry("800x600")
        self.window.configure(bg="#f4f4f4")
        self.window.resizable(True, True)

        # Style configuration
        self.header_color = "#2c3e50"  # Dark blue color for header
        self.button_color = "#3498db"  # Blue for buttons
        self.button_hover_color = "#2980b9"  # Darker blue for hover effect
        self.bg_color = "#ecf0f1"  # Light gray background

        self.create_ui()
        self.fetch_and_plot_data()

    def create_ui(self):
        # Header section
        header_frame = tk.Frame(self.window, bg=self.header_color, height=80)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Statistiques des Achats", font=("Arial", 20, "bold"), bg=self.header_color, fg="white").pack(pady=20)

        # Section for graph title
        tk.Label(self.window, text="Achats et Ventes par Jour", font=("Arial", 14, "bold"), bg=self.bg_color, fg="#2c3e50").pack(pady=10)

        # Graph container frame
        self.graph_frame = tk.Frame(self.window, bg=self.bg_color)
        self.graph_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Button to close the window
        close_button = tk.Button(self.window, text="Fermer", bg=self.button_color, fg="white", font=("Arial", 12, "bold"),
                                 activebackground=self.button_hover_color, command=self.window.destroy)
        close_button.pack(pady=20)

    def fetch_purchase_data(self):
        """ Fetch the purchase data (daily total) from the database. """
        conn = sqlite3.connect("pharma_users.db")
        cursor = conn.cursor()

        # Query to get daily purchase data (Total purchases per day)
        cursor.execute('''
            SELECT date, SUM(total_net) 
            FROM ventes
            GROUP BY date
            ORDER BY date
        ''')
        data = cursor.fetchall()
        conn.close()

        # Convert fetched data to a pandas DataFrame for easy manipulation
        df = pd.DataFrame(data, columns=['date', 'total_net'])
        df['date'] = pd.to_datetime(df['date'])  # Convert date to datetime format
        return df

    def plot_purchase_statistics(self):
        """ Plot both the purchase data and number of sales on a graph. """
        df = self.fetch_purchase_data()

        if not df.empty:
            # Create a plot (two lines showing daily purchases and daily sales)
            fig, ax = plt.subplots(figsize=(10, 5))

            # Plot the total_net (purchases)
            ax.plot(df['date'], df['total_net'], marker='o', linestyle='-', color='#3498db', label='Achats (Total Net)')

            # Query to get the total number of sales per day
            conn = sqlite3.connect("pharma_users.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT date, COUNT(*) 
                FROM ventes
                GROUP BY date
                ORDER BY date
            ''')
            sales_data = cursor.fetchall()
            conn.close()

            # Convert sales data into a pandas DataFrame for easy manipulation
            sales_df = pd.DataFrame(sales_data, columns=['date', 'sales_count'])
            sales_df['date'] = pd.to_datetime(sales_df['date'])  # Ensure date is datetime

            # Plot the number of sales
            ax.plot(sales_df['date'], sales_df['sales_count'], marker='s', linestyle='-', color='#e74c3c', label='Ventes (Nombre)')

            ax.set_title('Ventes et Achats par Jour', fontsize=16, fontweight="bold")
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Montant Total (TND) / Nombre de Ventes', fontsize=12)
            ax.grid(True)
            ax.legend()

            # Embed the plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)
            canvas.draw()

        else:
            # If there's no data, display a message
            tk.Label(self.graph_frame, text="Aucune donnée disponible.", font=("Arial", 12), bg=self.bg_color, fg="#e74c3c").pack(pady=20)

    def fetch_and_plot_data(self):
        """ Fetch data and plot it on the window. """
        self.plot_purchase_statistics()


# Example usage:
# root = tk.Tk()
# StatistiquesWindow(root)
# root.mainloop()
