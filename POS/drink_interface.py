import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
from datetime import datetime

class DrinksInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Drinks Interface")

        self.create_drinks_list()
        self.load_drinks_orders()
        self.update_time()  # Initial time update
        self.refresh_drinks_orders_periodically()

    def create_drinks_list(self):
        self.drinks_frame = tk.Frame(self.root, width=800, bg="black")
        self.drinks_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.drinks_frame, text="Drinks Orders", font=("Courier", 18), bg="black", fg="white").pack(pady=10)

        self.content_frame = tk.Frame(self.drinks_frame, bg="black")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.drinks_canvas = tk.Canvas(self.content_frame, bg="black")
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.drinks_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.drinks_canvas, style="My.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.drinks_canvas.configure(
                scrollregion=self.drinks_canvas.bbox("all")
            )
        )

        self.drinks_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.drinks_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.drinks_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bottom frame to hold time and pending labels
        self.bottom_frame = tk.Frame(self.content_frame, bg="black")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.time_label = tk.Label(self.bottom_frame, text="", font=("Courier", 12), bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.pending_label = tk.Label(self.bottom_frame, text="", font=("Courier", 12), bg="black", fg="white")
        self.pending_label.pack(side=tk.RIGHT, padx=10, pady=10)

        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Serve", font=("Courier", 16), command=self.serve_drink_order, bg="#007acc", fg="black").pack(pady=10)

    def load_drinks_orders(self):
        conn = sqlite3.connect('pos_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, order_details, status FROM drink_orders WHERE status='Pending'")
        all_orders = cursor.fetchall()
        conn.close()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        drink_orders = []
        for order in all_orders:
            order_id, order_details, status = order
            
            try:
                order_details = json.loads(order_details)
            except json.JSONDecodeError:
                order_details = {}

            # Debug: Print the order details for verification
            print(f"Order ID: {order_id}, Details: {order_details}")

            # Check if the order contains "Coke"
            if 'Coke' in order_details:
                print(f"Order ID: {order_id} contains Coke")  # Debug statement
                drink_orders.append(order)
            else:
                print(f"Order ID: {order_id} does not contain Coke")  # Debug statement

        displayed_drinks_orders = 0
        for i, drink_order in enumerate(drink_orders[:6]):  # Display up to the first six drink orders
            order_id, order_details, status = drink_order
            
            try:
                order_details = json.loads(order_details)
            except json.JSONDecodeError:
                order_details = {}
            
            border_frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            border_frame.grid(row=i//3, column=i%3, padx=10, pady=10)

            drink_order_frame = tk.Frame(border_frame, bg="black", bd=0, height=500, width=350)
            drink_order_frame.pack(padx=1, pady=1)  # Padding to create a thin border

            drink_order_frame.grid_propagate(False)  # Ensure the frame does not auto-resize

            tk.Label(drink_order_frame, text=f"Order ID: {order_id}", font=("Courier", 28), bg="black", fg="white", anchor="w").pack(fill="x", padx=20, pady=20)
            for item_name, details in order_details.items():
                quantity = details['quantity']
                tk.Label(drink_order_frame, text=f"{item_name} x{quantity}", font=("Courier", 22), bg="black", fg="white", anchor="w").pack(fill="x", padx=20, pady=10)

            displayed_drinks_orders += 1

        pending_count = len(drink_orders) - displayed_drinks_orders
        self.pending_label.config(text=f"Pending Orders: {pending_count}")

    def refresh_drinks_orders_periodically(self):
        self.load_drinks_orders()
        self.update_time()  # Update time periodically
        self.root.after(5000, self.refresh_drinks_orders_periodically)  # Refresh every 5 seconds

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1, self.update_time)  # Update time every millisecond

    def serve_drink_order(self):
        conn = sqlite3.connect('pos_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM drink_orders WHERE status='Pending' ORDER BY id ASC LIMIT 1")  # Get the first pending drink order
        first_order = cursor.fetchone()

        if first_order:
            order_id = first_order[0]
            cursor.execute("UPDATE drink_orders SET status='Completed' WHERE id=?", (order_id,))
            conn.commit()
            conn.close()

            self.load_drinks_orders()
        else:
            messagebox.showwarning("No Pending Orders", "There are no pending drink orders to mark as completed.")

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure("My.TFrame", background="black")
    app = DrinksInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
