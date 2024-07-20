import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import threading
import time
import json
from manager_codes import is_valid_manager  # Import the manager code validation function

class POS:
    def __init__(self, root):
        self.root = root
        self.root.title("MCDPOS")

        self.order = {'food': {}, 'drinks': {}}
        self.temp_quantity = 1
        self.promo_item = None

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.LEFT, expand=1, fill='both')
        self.create_frames()
        self.create_order_summary()
        self.create_main_menu()
        self.create_crew_menu()
        self.create_manager_menu()

    def create_frames(self):
        self.main_menu_frame = tk.Frame(self.notebook, bg="#d3d3d3")
        self.notebook.add(self.main_menu_frame, text="Main Menu")
        self.crew_menu_frame = tk.Frame(self.notebook, bg="#d3d3d3")
        self.notebook.add(self.crew_menu_frame, text="Crew Menu")
        self.manager_menu_frame = tk.Frame(self.notebook, bg="#d3d3d3")
        self.notebook.add(self.manager_menu_frame, text="Manager Menu")

    def create_order_summary(self):
        order_frame = tk.Frame(self.root, width=200, bg="#d3d3d3")
        order_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        tk.Label(order_frame, text="Order Summary", font=("Arial", 16), bg="#d3d3d3", fg="black").pack(pady=10)
        self.order_listbox = tk.Listbox(order_frame, bg="#ffffff", fg="black")
        self.order_listbox.pack(fill=tk.BOTH, expand=True)
        self.total_label = tk.Label(order_frame, text="Total: $0.00", font=("Arial", 16), bg="#d3d3d3", fg="black")
        self.total_label.pack(pady=10)
        button_frame = tk.Frame(order_frame, bg="#d3d3d3")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Checkout", font=("Arial", 14), command=self.checkout, bg="#007acc", fg="black").grid(row=0, column=0, padx=10)
        control_frame = tk.Frame(self.root, width=200, bg="#d3d3d3")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        tk.Button(control_frame, text="Manager", font=("Arial", 14), command=self.prompt_manager_login, bg="#007acc", fg="black").pack(pady=10)
        tk.Button(control_frame, text="Crew\nMenu", font=("Arial", 14), command=lambda: self.notebook.select(self.crew_menu_frame), bg="#007acc", fg="black").pack(pady=10)
        tk.Button(control_frame, text="Void", font=("Arial", 14), command=self.void_item, bg="#FF6666", fg="black").pack(pady=10)

    def create_number_row(self, parent_frame):
        number_frame = tk.Frame(parent_frame, bg="#d3d3d3")
        number_frame.grid(row=0, column=0, columnspan=4, pady=10)
        for i in range(10):
            tk.Button(number_frame, text=str(i), font=("Arial", 18), bg="#ffffff", fg="black", command=lambda i=i: self.set_quantity(i)).grid(row=0, column=i, padx=5, pady=5)
        number_frame.grid_columnconfigure(list(range(10)), weight=1)
        number_frame.grid_rowconfigure(0, weight=1)

    def create_main_menu(self):
        self.create_number_row(self.main_menu_frame)
        self.create_item_grid(self.main_menu_frame)

    def create_item_grid(self, parent_frame):
        items = self.load_menu_items_from_db()
        row, col = 1, 0
        for item in items:
            frame = tk.Frame(parent_frame, width=150, height=120, bg="#e6e6e6", highlightbackground="black", highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5)
            frame.grid_propagate(False)
            item_name, item_price, item_type = item[1], float(item[2]), item[3]
            tk.Button(frame, text=f"{item_name}\n${item_price:.2f}", font=("Arial", 14), bg="#e6e6e6", fg="black", command=lambda i=item: self.add_to_order(i)).place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)
            col += 1
            if col == 4:
                col = 0
                row += 1

    def create_crew_menu(self):
        tk.Label(self.crew_menu_frame, text="Crew Menu", font=("Arial", 20), bg="#d3d3d3", fg="black").pack(pady=20)
        tk.Button(self.crew_menu_frame, text="Promo\nItem", font=("Arial", 14), command=self.prompt_manager_login, bg="#ff6666", fg="black").pack(pady=10)

    def create_manager_menu(self):
        tk.Label(self.manager_menu_frame, text="Manager Menu", font=("Arial", 20), bg="#d3d3d3", fg="black").pack(pady=20)
        tk.Button(self.manager_menu_frame, text="Edit Menu Items", font=("Arial", 14), command=self.edit_menu_items, bg="#007acc", fg="black").pack(pady=10)

    def set_quantity(self, quantity):
        self.temp_quantity = quantity

    def add_to_order(self, item):
        item_name, item_price, item_type = item[1], float(item[2]), item[3]
        quantity = self.temp_quantity if self.temp_quantity else 1
        order_category = 'food' if item_type == 'food' else 'drinks'

        if item_name in self.order[order_category]:
            self.order[order_category][item_name]['quantity'] += quantity
            self.order[order_category][item_name]['total'] += item_price * quantity if self.promo_item != item_name else 0
        else:
            self.order[order_category][item_name] = {'quantity': quantity, 'total': item_price * quantity if self.promo_item != item_name else 0}

        self.update_order_list()
        self.update_total()
        self.temp_quantity = 1

    def update_order_list(self):
        self.order_listbox.delete(0, tk.END)
        for category, items in self.order.items():
            for item_name, details in items.items():
                promo_text = " 1P" if item_name == self.promo_item else ""
                self.order_listbox.insert(tk.END, f"{item_name} x{details['quantity']} - ${details['total']:.2f}{promo_text}")

    def update_total(self):
        total = sum(details['total'] for category in self.order.values() for details in category.values())
        self.total_label.config(text=f"Total: ${total:.2f}")

    def checkout(self):
        def perform_checkout():
            try:
                conn = sqlite3.connect('pos_system.db')
                cursor = conn.cursor()

                # Insert food orders
                food_order_details = json.dumps(self.order['food'])
                food_total_price = sum(details['total'] for details in self.order['food'].values())
                cursor.execute("INSERT INTO orders (order_details, total_price, status) VALUES (?, ?, 'Pending')",
                               (food_order_details, food_total_price))
                
                # Insert drink orders to a separate table
                drink_order_details = json.dumps(self.order['drinks'])
                drink_total_price = sum(details['total'] for details in self.order['drinks'].values())
                cursor.execute("INSERT INTO drink_orders (order_details, total_price, status) VALUES (?, ?, 'Pending')",
                               (drink_order_details, drink_total_price))

                conn.commit()
                conn.close()
                messagebox.showinfo("Checkout", "Order has been placed!")
                self.order = {'food': {}, 'drinks': {}}
                self.update_order_list()
                self.total_label.config(text="Total: $0.00")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

        self.root.after(0, perform_checkout)

    def void_item(self):
        selected_index = self.order_listbox.curselection()
        if selected_index:
            item_text = self.order_listbox.get(selected_index)
            item_name = item_text.split(' x')[0]
            for category in self.order:
                if item_name in self.order[category]:
                    del self.order[category][item_name]
                    break
            self.update_order_list()
            self.update_total()
        else:
            messagebox.showwarning("No Item Selected", "Please select an item from the order list first.")

    def prompt_manager_login(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Manager Login")
        tk.Label(self.login_window, text="Enter Username and Password", font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(self.login_window, font=("Arial", 14), justify='center')
        self.username_entry.pack(pady=5)
        self.password_entry = tk.Entry(self.login_window, font=("Arial", 14), justify='center', show='*')
        self.password_entry.pack(pady=5)
        self.create_keypad(self.login_window)
        tk.Button(self.login_window, text="Login", font=("Arial", 14), command=self.validate_manager_login, bg="#007acc", fg="black").pack(pady=20)

    def create_keypad(self, parent):
        keypad_frame = tk.Frame(parent)
        keypad_frame.pack(pady=10)
        def append_to_entry(entry, value):
            entry.insert(tk.END, value)
        def clear_entry(entry):
            entry.delete(0, tk.END)
        for i in range(10):
            tk.Button(keypad_frame, text=str(i), font=("Arial", 18), bg="white", fg="black", command=lambda i=i: append_to_entry(self.username_entry if self.username_entry.focus_get() else self.password_entry, i)).grid(row=i//3, column=i%3, padx=5, pady=5)
        tk.Button(keypad_frame, text="Clear", font=("Arial", 18), bg="white", fg="black", command=lambda: clear_entry(self.username_entry if self.username_entry.focus_get() else self.password_entry)).grid(row=3, column=1, padx=5, pady=5)

    def validate_manager_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if is_valid_manager(username, password):
            self.login_window.destroy()
            self.set_promo_item()
        else:
            messagebox.showerror("Access Denied", "Incorrect username or password.")

    def edit_menu_items(self):
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Edit Menu Items")
        tk.Label(editor_window, text="Edit Menu Items", font=("Arial", 16)).pack(pady=10)
        menu_frame = tk.Frame(editor_window)
        menu_frame.pack(pady=10)
        self.menu_listbox = tk.Listbox(menu_frame, selectmode=tk.SINGLE, bg="#ffffff", fg="black")
        self.menu_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_menu_items()
        button_frame = tk.Frame(editor_window)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Add Item", font=("Arial", 12), command=self.add_menu_item, bg="#007acc", fg="black").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Edit Item", font=("Arial", 12), command=self.edit_menu_item, bg="#007acc", fg="black").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Delete Item", font=("Arial", 12), command=self.delete_menu_item, bg="#007acc", fg="black").grid(row=0, column=2, padx=5, pady=5)

    def load_menu_items(self):
        items = self.load_menu_items_from_db()
        self.menu_listbox.delete(0, tk.END)
        for item in items:
            self.menu_listbox.insert(tk.END, f"{item[0]}: {item[1]} - ${item[2]:.2f} ({item[3]})")

    def load_menu_items_from_db(self):
        conn = sqlite3.connect('pos_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, type FROM menu_items")
        items = cursor.fetchall()
        conn.close()
        return items

    def add_menu_item(self):
        name = simpledialog.askstring("Item Name", "Enter the name of the new item:")
        price = simpledialog.askfloat("Item Price", "Enter the price of the new item:")
        item_type = simpledialog.askstring("Item Type", "Enter the type of the new item (food/drinks):")
        if name and price is not None and item_type in ['food', 'drinks']:
            conn = sqlite3.connect('pos_system.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO menu_items (name, price, type) VALUES (?, ?, ?)", (name, price, item_type))
            conn.commit()
            conn.close()
            self.load_menu_items()

    def edit_menu_item(self):
        selected_index = self.menu_listbox.curselection()
        if selected_index:
            selected_item = self.menu_listbox.get(selected_index).split(": ")
            item_id = int(selected_item[0])
            current_name, current_price, current_type = selected_item[1].split(" - $")[0], float(selected_item[1].split(" - $")[1].split(" ")[0]), selected_item[1].split("(")[1][:-1]
            new_name = simpledialog.askstring("Edit Item Name", "Enter the new name of the item:", initialvalue=current_name)
            new_price = simpledialog.askfloat("Edit Item Price", "Enter the new price of the item:", initialvalue=current_price)
            new_type = simpledialog.askstring("Edit Item Type", "Enter the new type of the item (food/drinks):", initialvalue=current_type)
            if new_name and new_price is not None and new_type in ['food', 'drinks']:
                conn = sqlite3.connect('pos_system.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE menu_items SET name = ?, price = ?, type = ? WHERE id = ?", (new_name, new_price, new_type, item_id))
                conn.commit()
                conn.close()
                self.load_menu_items()

    def delete_menu_item(self):
        selected_index = self.menu_listbox.curselection()
        if selected_index:
            selected_item = self.menu_listbox.get(selected_index).split(": ")
            item_id = int(selected_item[0])
            conn = sqlite3.connect('pos_system.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
            conn.commit()
            conn.close()
            self.load_menu_items()

    def set_promo_item(self):
        selected_index = self.order_listbox.curselection()
        if selected_index:
            item_text = self.order_listbox.get(selected_index)
            item_name = item_text.split(' x')[0]
            for category in self.order:
                if item_name in self.order[category]:
                    self.promo_item = item_name
                    self.order[category][item_name]['total'] = 0
                    self.update_order_list()
                    self.update_total()
                    messagebox.showinfo("Promo Item", f"{self.promo_item} is now free!")

def show_splash_screen():
    splash = tk.Toplevel(root)
    splash.title("Loading...")
    splash.geometry("300x150")
    splash_label = tk.Label(splash, text="Loading MCDPOS...", font=("Arial", 14))
    splash_label.pack(pady=20)
    progress = ttk.Progressbar(splash, orient="horizontal", length=250, mode="determinate")
    progress.pack(pady=10)
    progress.start()
    def close_splash():
        time.sleep(2)
        splash.destroy()
        main_app()
    threading.Thread(target=close_splash).start()

def main_app():
    app = POS(root)
    root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_splash_screen()
    root.mainloop()
