import sqlite3
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet
from crypt import new_key  
from pss_f_send import *




class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.configure(bg='black')
        self.root.geometry("600x400")
        self.cipher = None

        self.create_login_frame()

        setup_db()

    def create_login_frame(self):
        frame = Frame(self.root, bg='black')
        frame.pack(pady=20)

        btn_login = Button(frame, text="Login (load key file)", command=self.login)
        btn_login.grid(row=0, column=0, padx=5)
        btn_signup = Button(frame, text="Signup (new key)", command=self.signup)
        btn_signup.grid(row=0, column=1, padx=5)

    def login(self):
        f = filedialog.askopenfile(mode='rb', title='Open master key file', filetypes=[('All files','*.*')])
        if f:
            key = f.read()
            try:
                self.cipher = Fernet(key)
                f.close()
                self.show_main_widgets()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid key file: {e}")

    def signup(self):
        key = new_key()
        f = filedialog.asksaveasfile(mode='wb', defaultextension='.bin', title="Save new master key")
        if f:
            f.write(key)
            f.close()
            self.cipher = Fernet(key)
            messagebox.showinfo("Key saved", "Master key saved. Keep it safe!")
            self.show_main_widgets()
    def decrypt(self):
        pass


    def show_main_widgets(self):
        for w in self.root.winfo_children():
            w.destroy()
        # input frame
        input_frame = Frame(self.root, bg='black')
        input_frame.pack(pady=10)
        
        Label(input_frame, text="Service:", bg='black', fg='white').grid(row=0, column=0, sticky=E, padx=5, pady=5)
        self.service_entry = Entry(input_frame, width=20)
        self.service_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Username:", bg='black', fg='white').grid(row=0, column=2, sticky=E, padx=5, pady=5)
        self.uname_entry = Entry(input_frame, width=20)
        self.uname_entry.grid(row=0, column=3, padx=5, pady=5)

        Label(input_frame, text="Password:", bg='black', fg='white').grid(row=1, column=0, sticky=E, padx=5, pady=5)
        self.pwd_entry = Entry(input_frame, width=44)
        self.pwd_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        btn_insert = Button(input_frame, text="Insert / Save", command=self.insert_record)
        btn_insert.grid(row=2, column=1, pady=5)

        btn_fetch = Button(input_frame, text="Fetch", command=self.fetch_records)
        btn_fetch.grid(row=2, column=2, pady=5)

        btn_delete = Button(input_frame, text="Delete", command=self.delete_records)
        btn_delete.grid(row=2, column=3, pady=5)

        btn_show=Button(text='Show passwords',command=self.decrypt)
        btn_show.grid(row=3,column=4,pady=5)

        btn_clear = Button(input_frame, text="Clear Inputs", command=self.clear_inputs)
        btn_clear.grid(row=3, column=1, columnspan=3, pady=5)

        # Treeview to show records/results
        self.tree = ttk.Treeview(self.root, columns=("service","username","password"), show='headings', height=8)
        self.tree.heading("service", text="Service")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Encrypted/Password")

        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def insert_record(self):
        svc = self.service_entry.get().strip()
        uname = self.uname_entry.get().strip()
        pwd = self.pwd_entry.get().strip()
        if not svc or not uname or not pwd:
            messagebox.showwarning("Input error", "Please fill service, username, and password")
            return
        token = self.cipher.encrypt(pwd.encode())
        send(svc, uname, token)
        messagebox.showinfo("Saved", "Credentials saved (encrypted).")
        self.clear_inputs()

    def fetch_records(self):
        svc = self.service_entry.get().strip()
        uname = self.uname_entry.get().strip()
        if not svc:
            messagebox.showwarning("Input error", "Please specify a service to fetch")
            return
        rows = receive(svc, uname or None)
        self.refresh_tree(rows)

    def delete_records(self):
        svc = self.service_entry.get().strip()
        uname = self.uname_entry.get().strip()
        if not svc:
            messagebox.showwarning("Input error", "Please specify at least service for delete")
            return
        resp = messagebox.askyesno("Confirm delete", 
            f"Delete records for service = '{svc}'" + (f", user = '{uname}'" if uname else "") + "?")
        if not resp:
            return
        delete(svc, uname or None)
        messagebox.showinfo("Deleted", "Records deleted (if any).")
        self.refresh_tree([])

    def refresh_tree(self, rows):
        # clear existing
        for i in self.tree.get_children():
            self.tree.delete(i)
        # insert new rows
        for r in rows:
            svc, uname, pwd = r
            self.tree.insert('', END, values=(svc, uname, pwd))

    def clear_inputs(self):
        self.service_entry.delete(0, END)
        self.uname_entry.delete(0, END)
        self.pwd_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
