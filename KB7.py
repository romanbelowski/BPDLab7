import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import webbrowser

class FileViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Viewer Demo")
        self.root.geometry("800x600")
        
        # Registration status
        self.is_registered = False
        self.key = None
        
        # Create main menu
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="File Properties", command=self.show_properties)
        
        # Encryption menu
        encryption_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Encryption", menu=encryption_menu)
        encryption_menu.add_command(label="Encrypt Text", command=self.encrypt_text)
        encryption_menu.add_command(label="Decrypt Text", command=self.decrypt_text)
        
        # Help menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="Register", command=self.show_registration)
        
        # Text area
        self.text_area = tk.Text(root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        
        # Status bar
        self.status_bar = ttk.Label(root, text="Ready")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def encrypt_text(self):
        if not self.is_registered:
            messagebox.showwarning("Registration Required", 
                                 "Please register to use the encryption feature")
            return
        
        # Create encryption window
        encrypt_window = tk.Toplevel(self.root)
        encrypt_window.title("Encrypt Text")
        encrypt_window.geometry("300x100")
        
        ttk.Label(encrypt_window, text="Enter encryption key:").pack(pady=5)
        key_entry = ttk.Entry(encrypt_window)
        key_entry.pack(pady=5)
        
        def perform_encryption():
            encryption_key = key_entry.get()
            if not encryption_key:
                messagebox.showerror("Error", "Please enter an encryption key")
                return
                
            text = self.text_area.get(1.0, tk.END).strip()
            if not text:
                messagebox.showerror("Error", "No text to encrypt")
                return
                
            encrypted_text = self.vigenere_encrypt(text, encryption_key)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, encrypted_text)
            self.status_bar.config(text="Text encrypted successfully")
            encrypt_window.destroy()
            
        ttk.Button(encrypt_window, text="Encrypt", command=perform_encryption).pack(pady=5)

    def decrypt_text(self):
        if not self.is_registered:
            messagebox.showwarning("Registration Required", 
                                 "Please register to use the decryption feature")
            return
        
        # Create decryption window
        decrypt_window = tk.Toplevel(self.root)
        decrypt_window.title("Decrypt Text")
        decrypt_window.geometry("300x100")
        
        ttk.Label(decrypt_window, text="Enter decryption key:").pack(pady=5)
        key_entry = ttk.Entry(decrypt_window)
        key_entry.pack(pady=5)
        
        def perform_decryption():
            decryption_key = key_entry.get()
            if not decryption_key:
                messagebox.showerror("Error", "Please enter a decryption key")
                return
                
            text = self.text_area.get(1.0, tk.END).strip()
            if not text:
                messagebox.showerror("Error", "No text to decrypt")
                return
                
            decrypted_text = self.vigenere_decrypt(text, decryption_key)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, decrypted_text)
            self.status_bar.config(text="Text decrypted successfully")
            decrypt_window.destroy()
            
        ttk.Button(decrypt_window, text="Decrypt", command=perform_decryption).pack(pady=5)
        
    def vigenere_encrypt(self, text, key):
        encrypted = ""
        key_length = len(key)
        key_as_int = [ord(i) for i in key]
        text_int = [ord(i) for i in text]
        for i in range(len(text_int)):
            if text[i].isalpha():
                value = (text_int[i] + key_as_int[i % key_length]) % 26
                encrypted += chr(value + 65)
            else:
                encrypted += text[i]
        return encrypted
        
    def vigenere_decrypt(self, text, key):
        decrypted = ""
        key_length = len(key)
        key_as_int = [ord(i) for i in key]
        text_int = [ord(i) for i in text]
        for i in range(len(text_int)):
            if text[i].isalpha():
                value = (text_int[i] - key_as_int[i % key_length]) % 26
                decrypted += chr(value + 65)
            else:
                decrypted += text[i]
        return decrypted
        
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                self.status_bar.config(text=f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
                
    def print_file(self):
        if not self.is_registered:
            messagebox.showwarning("Registration Required", 
                                 "Please register to use the print feature")
            return
        content = self.text_area.get(1.0, tk.END)
        # Print simulation
        messagebox.showinfo("Print", "Document sent to printer")
        
    def find_text(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Find")
        search_window.geometry("300x100")
        
        ttk.Label(search_window, text="Find:").pack(pady=5)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)
        
        def search():
            keyword = search_entry.get()
            content = self.text_area.get(1.0, tk.END)
            if keyword in content:
                messagebox.showinfo("Found", f"Found '{keyword}' in text")
            else:
                messagebox.showinfo("Not Found", f"Could not find '{keyword}'")
                
        ttk.Button(search_window, text="Find", command=search).pack(pady=5)
        
    def show_properties(self):
        content = self.text_area.get(1.0, tk.END)
        char_count = len(content)
        word_count = len(content.split())
        
        properties = f"""Document Properties:
        Characters: {char_count}
        Words: {word_count}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        messagebox.showinfo("Properties", properties)
        
    def show_about(self):
        about_text = """File Viewer Demo
        Version 1.0
        
        A demonstration of software protection methods
        This is a Demoware version with disabled save functionality
        Features:
        - Text file viewing
        - Text encryption/decryption using Vigenere cipher
        - Text search
        - File properties
        - Print feature (requires registration)
        """
        messagebox.showinfo("About", about_text)
        
    def show_docs(self):
        docs_text = """Documentation:
        
        This is a simple file viewer with basic functionality.
        - Open: Opens text files
        - Print: Prints the current document (requires registration)
        - Find: Searches for text in the document
        - Properties: Shows document statistics
        - Encrypt: Encrypts text using Vigenere cipher (requires registration)
        - Decrypt: Decrypts text using Vigenere cipher (requires registration)
        
        Note: Save functionality is disabled in demo version
        """
        messagebox.showinfo("Documentation", docs_text)
        
    def show_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Registration")
        reg_window.geometry("300x150")
        
        ttk.Label(reg_window, text="Enter Registration Key:").pack(pady=5)
        key_entry = ttk.Entry(reg_window)
        key_entry.pack(pady=5)
        
        def verify_key():
            entered_key = key_entry.get()
            if self.verify_registration_key(entered_key):
                self.is_registered = True
                self.key = entered_key
                messagebox.showinfo("Success", "Registration successful!")
                reg_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid registration key")
                
        ttk.Button(reg_window, text="Register", command=verify_key).pack(pady=5)
        
    def verify_registration_key(self, key):
        # Simple verification - in real application would be more secure
        return bool(key and len(key) >= 8)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileViewer(root)
    root.mainloop()