import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json

class OrdersInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Orders Interface")

        self.create_order_list()
        self.load_orders()
        self.refresh_orders_periodically()

    def create_order_list(self):
        self.order_frame = tk.Frame(self.root, width=800, bg="black")
        self.order_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.order_frame, text="Orders", font=("Courier", 18), bg="black", fg="white").pack(pady=10)

        self.content_frame = tk.Frame(self.order_frame, bg="black")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.order_canvas = tk.Canvas(self.content_frame, bg="black")
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.order_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.order_canvas, style="My.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.order_canvas.configure(
                scrollregion=self.order_canvas.bbox("all")
            )
        )

        self.order_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.order_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.order_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.pending_label = tk.Label(self.content_frame, text="", font=("Courier", 12), bg="black", fg="white")
        self.pending_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Serve", font=("Courier", 16), command=self.serve_order, bg="#007acc", fg="black").pack(pady=10)

    def load_orders(self):
        conn = sqlite3.connect('pos_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, order_details, total_price, status FROM orders WHERE status='Pending'")
        orders = cursor.fetchall()
        conn.close()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        displayed_orders = 0
        for i, order in enumerate(orders[:2]):  # Display only the first two orders
            order_id, order_details, total_price, status = order
            order_details = json.loads(order_details)

            border_frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            border_frame.grid(row=0, column=i, padx=10, pady=10)

            order_frame = tk.Frame(border_frame, bg="black", bd=0, height=500, width=350)
            order_frame.pack(padx=1, pady=1)  # Padding to create a thin border

            order_frame.grid_propagate(False)  # Ensure the frame does not auto-resize

            tk.Label(order_frame, text=f"Order ID: {order_id}", font=("Courier", 28), bg="black", fg="white", anchor="w").pack(fill="x", padx=20, pady=20)
            for item_name, details in order_details.items():
                quantity = details['quantity']
                tk.Label(order_frame, text=f"{item_name} x{quantity}", font=("Courier", 22), bg="black", fg="white", anchor="w").pack(fill="x", padx=20, pady=10)

            displayed_orders += 1

        pending_count = len(orders) - displayed_orders
        self.pending_label.config(text=f"Pending Orders: {pending_count}")

    def refresh_orders_periodically(self):
        self.load_orders()
        self.root.after(5000, self.refresh_orders_periodically)  # Refresh every 5 seconds

    def serve_order(self):
        conn = sqlite3.connect('pos_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM orders WHERE status='Pending' ORDER BY id ASC LIMIT 1")  # Get the first pending order
        first_order = cursor.fetchone()

        if first_order:
            order_id = first_order[0]
            cursor.execute("UPDATE orders SET status='Completed' WHERE id=?", (order_id,))
            conn.commit()
            conn.close()

            self.load_orders()
        else:
            messagebox.showwarning("No Pending Orders", "There are no pending orders to mark as completed.")

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure("My.TFrame", background="black")
    app = OrdersInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
