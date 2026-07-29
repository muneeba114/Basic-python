import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Global variable balance store karne ke liye
balance = 0.0

# ---------------- Functions ----------------

def deposit_money():
    global balance
    try:
        amount = float(entry_amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Barae meherbani 0 se zyada amount enter karein!")
        else:
            balance += amount
            time_now = datetime.now().strftime("%H:%M:%S")
            
            # History me record add karna
            history_list.insert(tk.END, f"[{time_now}] Deposit: +PKR {amount:.2f}")
            history_list.itemconfig(tk.END, {'fg': 'green'})
            
            messagebox.showinfo("Success", f"PKR {amount:.2f} successfully deposit ho gaye hain!")
            entry_amount.delete(0, tk.END)
            update_balance_display()
    except ValueError:
        messagebox.showerror("Error", "Sahi number enter karein!")

def withdraw_money():
    global balance
    try:
        amount = float(entry_amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Barae meherbani 0 se zyada amount enter karein!")
        elif amount > balance:
            messagebox.showerror("Error", "Aapke account me itna balance nahi hai!")
        else:
            balance -= amount
            time_now = datetime.now().strftime("%H:%M:%S")
            
            # History me record add karna
            history_list.insert(tk.END, f"[{time_now}] Withdraw: -PKR {amount:.2f}")
            history_list.itemconfig(tk.END, {'fg': 'red'})
            
            messagebox.showinfo("Success", f"PKR {amount:.2f} successfully withdraw ho gaye hain!")
            entry_amount.delete(0, tk.END)
            update_balance_display()
    except ValueError:
        messagebox.showerror("Error", "Sahi number enter karein!")

def show_balance():
    messagebox.showinfo("Current Balance", f"Aapka meojooda balance hai: PKR {balance:.2f}")

def update_balance_display():
    label_balance.config(text=f"Current Balance: PKR {balance:.2f}")

def clear_history():
    history_list.delete(0, tk.END)

# ---------------- GUI Setup ----------------

root = tk.Tk()
root.title("Bank Management System")
root.geometry("420x550")
root.config(bg="#f0f2f5")

# Heading
title_label = tk.Label(root, text="Bank Management System", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#1a73e8")
title_label.pack(pady=10)

# Balance Display Label
label_balance = tk.Label(root, text="Current Balance: PKR 0.00", font=("Arial", 12, "bold"), bg="#f0f2f5", fg="#333")
label_balance.pack(pady=5)

# Amount Input Label & Entry
label_input = tk.Label(root, text="Amount Enter Karein:", font=("Arial", 10), bg="#f0f2f5")
label_input.pack(pady=(10, 2))

entry_amount = tk.Entry(root, font=("Arial", 12), justify="center", width=20)
entry_amount.pack(pady=5)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f0f2f5")
btn_frame.pack(pady=10)

# Deposit Button
btn_deposit = tk.Button(btn_frame, text="Deposit / Add", font=("Arial", 10, "bold"), bg="#28a745", fg="white", width=12, command=deposit_money)
btn_deposit.grid(row=0, column=0, padx=5, pady=5)

# Withdraw Button
btn_withdraw = tk.Button(btn_frame, text="Withdraw", font=("Arial", 10, "bold"), bg="#dc3545", fg="white", width=12, command=withdraw_money)
btn_withdraw.grid(row=0, column=1, padx=5, pady=5)

# Show Balance Button
btn_show = tk.Button(btn_frame, text="Show Balance", font=("Arial", 10, "bold"), bg="#17a2b8", fg="white", width=25, command=show_balance)
btn_show.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# ---------------- Transaction History Section ----------------

history_label = tk.Label(root, text="Transaction History:", font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#333")
history_label.pack(pady=(15, 2))

# Frame for Listbox and Scrollbar
history_frame = tk.Frame(root)
history_frame.pack(pady=5)

scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL)
history_list = tk.Listbox(history_frame, width=35, height=8, font=("Courier", 10), yscrollcommand=scrollbar.set)

scrollbar.config(command=history_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_list.pack(side=tk.LEFT, fill=tk.BOTH)

# Clear History Button
btn_clear = tk.Button(root, text="Clear History", font=("Arial", 9), bg="#6c757d", fg="white", command=clear_history)
btn_clear.pack(pady=5)

# App Loop
root.mainloop()