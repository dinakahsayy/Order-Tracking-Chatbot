import sqlite3
import tkinter as tk
from tkinter import messagebox

# Creating the database and inserting sample data
def create_database():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Log message for debugging
    print("Creating 'orders' table if it doesn't exist...")

    # Creating table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_number TEXT PRIMARY KEY,
            status TEXT,
            current_facility TEXT,
            shipment_date TEXT,
            expected_delivery_date TEXT,
            last_update TEXT
        )
    ''')

    # Sample data
    sample_orders = [
        ('1234', 'shipped', 'New York Distribution Center', '2024-09-25', '2024-10-02', 'Package is in transit to Richmond, VA.'),
        ('5678', 'delivered', 'Richmond, VA', '2024-09-18', '2024-09-20', 'Delivered on 2024-09-20.'),
        ('91011', 'in transit', 'Chicago Hub', '2024-09-24', '2024-10-03', 'Package left Chicago Hub at 5 PM.')
    ]

    # Inserting data into table
    cursor.executemany('''
        INSERT OR IGNORE INTO orders (order_number, status, current_facility, shipment_date, expected_delivery_date, last_update)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_orders)

    conn.commit()
    conn.close()

    # Log message for debugging
    print("Database setup complete. Sample data inserted.")

# Creating the chatbot to track orders
class OrderChatbotGUI:
    def __init__(self, root, db_file):
        self.root = root
        self.db_file = db_file

        # Setup GUI
        self.root.title("Order Tracking System")
        self.root.geometry("500x300")

        self.title_label = tk.Label(self.root, text="Order Tracking System", font=("Arial", 18))
        self.title_label.pack(pady=10)

        self.instruction_label = tk.Label(self.root, text="Please enter your order number:")
        self.instruction_label.pack()

        self.order_entry = tk.Entry(self.root, width=30)
        self.order_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Track Order", command=self.track_order)
        self.submit_button.pack(pady=5)

        self.result_area = tk.Text(self.root, height=8, width=50, state='disabled')
        self.result_area.pack(pady=10)

    def get_order_status(self, order_number):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Log order number the user is entering
        print(f"Fetching status for order number: {order_number}")

        cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
        order = cursor.fetchone()

        conn.close()
        return order

    def display_order_status(self, order_details):
        if order_details:
            order_number, status, current_facility, shipment_date, delivery_date, last_update = order_details
            status_text = (
                f"Order Number: {order_number}\n"
                f"Status: {status}\n"
                f"Current Facility: {current_facility}\n"
                f"Shipment Date: {shipment_date}\n"
                f"Expected Delivery Date: {delivery_date}\n"
                f"Last Update: {last_update}\n"
            )
        else:
            status_text = "Order not found."

        self.result_area.config(state='normal')
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, status_text)
        self.result_area.config(state='disabled')

    def track_order(self):
        order_number = self.order_entry.get()
        order_details = self.get_order_status(order_number)

        if order_details:
            self.display_order_status(order_details)
        else:
            messagebox.showerror("Order Not Found", f"Sorry, no details found for order number {order_number}.")

# Creating database and sample data
create_database()

# Run the chatbot GUI
root = tk.Tk()
chatbot = OrderChatbotGUI(root, 'orders.db')
root.mainloop()
