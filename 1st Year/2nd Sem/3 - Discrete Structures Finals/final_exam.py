import tkinter as tk
from tkinter import messagebox
import math

class SecureCommApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureComm")
        self.root.geometry("500x600")
        self.root.configure(bg="#F5F5F7")  # Apple Off-White background

        # --- Header Section ---
        tk.Label(root, text="SecureComm", font=("Helvetica Neue", 28, "bold"), 
                 bg="#F5F5F7", fg="#1D1D1F").pack(pady=(40, 5))
        tk.Label(root, text="Discrete Structures: Bijective Encryption", font=("Helvetica Neue", 11), 
                 bg="#F5F5F7", fg="#86868B").pack(pady=(0, 30))

        # --- Input Field ---
        self.create_label("Enter Secret Ballot")
        self.msg_entry = tk.Entry(root, width=30, font=("Helvetica Neue", 14), 
                                  bg="#FFFFFF", fg="#1D1D1F", relief="flat", 
                                  highlightthickness=1, highlightbackground="#D2D2D7",
                                  insertbackground="#007AFF")
        self.msg_entry.pack(pady=10, ipady=8)

        # --- Keys Section ---
        keys_frame = tk.Frame(root, bg="#F5F5F7")
        keys_frame.pack(pady=20)

        # Key A
        a_frame = tk.Frame(keys_frame, bg="#F5F5F7")
        a_frame.grid(row=0, column=0, padx=15)
        tk.Label(a_frame, text="Key 'a' (Multiplier)", font=("Helvetica Neue", 9), bg="#F5F5F7", fg="#86868B").pack()
        self.key_a_entry = tk.Entry(a_frame, width=8, font=("Helvetica Neue", 14), bg="#FFFFFF", 
                                    relief="flat", highlightthickness=1, highlightbackground="#D2D2D7", justify='center')
        self.key_a_entry.insert(0, "17")
        self.key_a_entry.pack(ipady=5)

        # Key B
        b_frame = tk.Frame(keys_frame, bg="#F5F5F7")
        b_frame.grid(row=0, column=1, padx=15)
        tk.Label(b_frame, text="Key 'b' (Shift)", font=("Helvetica Neue", 9), bg="#F5F5F7", fg="#86868B").pack()
        self.key_b_entry = tk.Entry(b_frame, width=8, font=("Helvetica Neue", 14), bg="#FFFFFF", 
                                    relief="flat", highlightthickness=1, highlightbackground="#D2D2D7", justify='center')
        self.key_b_entry.insert(0, "20")
        self.key_b_entry.pack(ipady=5)

        # --- Status Indicator ---
        self.status_label = tk.Label(root, text="Ready to Validate", 
                                     font=("Helvetica Neue", 10, "bold"), bg="#F5F5F7", fg="#86868B")
        self.status_label.pack(pady=10)

        # --- Action Button (Apple Blue) ---
        self.btn = tk.Button(root, text="Validate & Encrypt", command=self.process_encryption, 
                             bg="#007AFF", fg="white", font=("Helvetica Neue", 12, "bold"), 
                             relief="flat", activebackground="#005BB7", activeforeground="white",
                             cursor="hand2", width=20)
        self.btn.pack(pady=10, ipady=10)

        # --- Output Area ---
        self.create_label("Encrypted Ciphertext")
        self.result_box = tk.Text(root, height=3, width=32, font=("Helvetica Neue", 14), 
                                  bg="#E8E8ED", fg="#1D1D1F", relief="flat", state='disabled', padx=15, pady=15)
        self.result_box.pack(pady=10)

        # --- Footer ---
        tk.Label(root, text="Final Exam Submission | Allen Jerrome M. Tolete", 
                 font=("Helvetica Neue", 9), bg="#F5F5F7", fg="#A1A1A6").pack(side="bottom", pady=20)

    def create_label(self, text):
        tk.Label(self.root, text=text, bg="#F5F5F7", fg="#1D1D1F", font=("Helvetica Neue", 11, "bold")).pack()

    def affine_encrypt(self, text, a, b):
        res = ""
        for char in text.upper():
            if char.isalpha():
                p = ord(char) - 65
                res += chr(((a * p + b) % 26) + 65)
            else:
                res += char
        return res

    def process_encryption(self):
        try:
            a = int(self.key_a_entry.get())
            b = int(self.key_b_entry.get())
            msg = self.msg_entry.get()

            if not msg: return

            if math.gcd(a, 26) == 1:
                self.status_label.config(text="BIJECTION VALIDATED", fg="#34C759") # Apple Green
                self.display_result(self.affine_encrypt(msg, a, b))
            else:
                self.status_label.config(text="NOT BIJECTIVE", fg="#FF3B30") # Apple Red
                messagebox.showerror("Math Error", "Key 'a' and 26 must be coprime.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")

    def display_result(self, text):
        self.result_box.config(state='normal')
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, text)
        self.result_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureCommApp(root)
    root.mainloop()