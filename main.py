import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime

# PDF Invoice Class
class PDFInvoice(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'INVOICE', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_invoice_details(self, date, customer_ref, our_ref):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Date: {date}', 0, 1)
        self.cell(0, 10, f'Customer REF: {customer_ref}', 0, 1)
        self.cell(0, 10, f'Our REF: {our_ref}', 0, 1)
        self.ln(10)

    def add_client_info(self, client_name, client_address):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Bill To:', 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, client_name, 0, 1)
        self.cell(0, 10, client_address, 0, 1)
        self.ln(10)

    def add_items_table(self, items):
        self.set_font('Arial', 'B', 12)
        # Table Header
        self.cell(30, 10, 'Item nº', 1, 0, 'C')
        self.cell(80, 10, 'Description', 1, 0, 'C')
        self.cell(20, 10, 'Quantity', 1, 0, 'C')
        self.cell(30, 10, 'Unit Price', 1, 0, 'C')
        self.cell(30, 10, 'Total', 1, 1, 'C')
        self.set_font('Arial', '', 12)
        # Table Rows
        for item in items:
            self.cell(30, 10, item['item_no'], 1, 0, 'C')
            self.cell(80, 10, item['description'], 1, 0)
            self.cell(20, 10, str(item['quantity']), 1, 0, 'C')
            self.cell(30, 10, f"${item['unit_price']:.2f}", 1, 0, 'C')
            self.cell(30, 10, f"${item['quantity'] * item['unit_price']:.2f}", 1, 1, 'C')
        self.ln(10)

    def add_total(self, total):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Total Amount: ${total:.2f}', 0, 1)

# GUI Application
class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        self.root.geometry("500x400")

        # Labels and Entry Fields
        tk.Label(root, text="Client Name:").grid(row=0, column=0, padx=10, pady=5)
        self.client_name = tk.Entry(root)
        self.client_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Client Address:").grid(row=1, column=0, padx=10, pady=5)
        self.client_address = tk.Entry(root)
        self.client_address.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Customer REF:").grid(row=2, column=0, padx=10, pady=5)
        self.customer_ref = tk.Entry(root)
        self.customer_ref.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Our REF:").grid(row=3, column=0, padx=10, pady=5)
        self.our_ref = tk.Entry(root)
        self.our_ref.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Item nº:").grid(row=4, column=0, padx=10, pady=5)
        self.item_no = tk.Entry(root)
        self.item_no.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(root, text="Description:").grid(row=5, column=0, padx=10, pady=5)
        self.description = tk.Entry(root)
        self.description.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(root, text="Quantity:").grid(row=6, column=0, padx=10, pady=5)
        self.quantity = tk.Entry(root)
        self.quantity.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(root, text="Unit Price:").grid(row=7, column=0, padx=10, pady=5)
        self.unit_price = tk.Entry(root)
        self.unit_price.grid(row=7, column=1, padx=10, pady=5)

        # Add Item Button
        self.add_item_button = tk.Button(root, text="Add Item", command=self.add_item)
        self.add_item_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Generate Invoice Button
        self.generate_button = tk.Button(root, text="Generate Invoice", command=self.generate_invoice)
        self.generate_button.grid(row=9, column=0, columnspan=2, pady=10)

        # List to store items
        self.items = []

    def add_item(self):
        item_no = self.item_no.get()
        description = self.description.get()
        quantity = int(self.quantity.get())
        unit_price = float(self.unit_price.get())

        self.items.append({
            'item_no': item_no,
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price
        })

        messagebox.showinfo("Success", "Item added successfully!")
        self.item_no.delete(0, tk.END)
        self.description.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.unit_price.delete(0, tk.END)

    def generate_invoice(self):
        client_name = self.client_name.get()
        client_address = self.client_address.get()
        customer_ref = self.customer_ref.get()
        our_ref = self.our_ref.get()

        if not client_name or not client_address or not customer_ref or not our_ref or not self.items:
            messagebox.showerror("Error", "Please fill all fields and add at least one item!")
            return

        pdf = PDFInvoice()
        pdf.add_page()
        pdf.add_invoice_details(datetime.today().strftime('%Y-%m-%d'), customer_ref, our_ref)
        pdf.add_client_info(client_name, client_address)
        pdf.add_items_table(self.items)
        total = sum(item['quantity'] * item['unit_price'] for item in self.items)
        pdf.add_total(total)

        output_file = f"Invoice_{customer_ref}.pdf"
        pdf.output(output_file)
        messagebox.showinfo("Success", f"Invoice generated: {output_file}")

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()