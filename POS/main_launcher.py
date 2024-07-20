import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome")  # Changed the title to "Welcome"

        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#d3d3d3")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Launch Orders Interface", font=("Arial", 16),
                  command=self.launch_orders_interface, bg="#007acc", fg="black").pack(pady=10)
        
        tk.Button(button_frame, text="Launch Drinks Interface", font=("Arial", 16),
                  command=self.launch_drinks_interface, bg="#007acc", fg="black").pack(pady=10)
        
        tk.Button(button_frame, text="Launch POS System", font=("Arial", 16),
                  command=self.launch_pos_system, bg="#007acc", fg="black").pack(pady=10)

    def launch_orders_interface(self):
        subprocess.Popen(["python", "/Users/jackhodgy/Desktop/POS/order_interface.py"])

    def launch_drinks_interface(self):
        subprocess.Popen(["python", "/Users/jackhodgy/Desktop/POS/drink_interface.py"])

    def launch_pos_system(self):
        subprocess.Popen(["python", "/Users/jackhodgy/Desktop/POS/pos_system_database.py"])

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

