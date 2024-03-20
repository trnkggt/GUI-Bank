import tkinter as tk
import sqlite3
import datetime
import bcrypt
from tkinter import messagebox
from tkcalendar import Calendar
from database import create_user, create_connection, login_user


# ...

class RegisterWindow:
    def __init__(self, parent, bank_app):
        self.parent = parent
        self.bank_app = bank_app
        self.register_window = tk.Toplevel(parent)
        self.register_window.title("Register")

        # Increase the window size
        # self.register_window.geometry('320x260')

        # Create registration form elements here
        self.register_label = tk.Label(self.register_window,
                                       text="Registration Form",
                                       font=("Helvetica", 18, "bold"))
        self.register_label.grid(row=0, columnspan=2, pady=10)

        field_label_font = ("Helvetica", 12)

        self.name_label = tk.Label(self.register_window, text="Name:", font=field_label_font)
        self.name_label.grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.register_window, font=field_label_font)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.last_name_label = tk.Label(self.register_window, text="Last Name:", font=field_label_font)
        self.last_name_label.grid(row=2, column=0, padx=10, pady=5)
        self.last_name_entry = tk.Entry(self.register_window, font=field_label_font)
        self.last_name_entry.grid(row=2, column=1, padx=10, pady=5)

        self.id_number_label = tk.Label(self.register_window, text="ID number:", font=field_label_font)
        self.id_number_label.grid(row=3, column=0, padx=10, pady=5)
        self.id_number_entry = tk.Entry(self.register_window, font=field_label_font)
        self.id_number_entry.grid(row=3, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.register_window, text="Password:", font=field_label_font)
        self.password_label.grid(row=4, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.register_window, show="*", font=field_label_font)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5)

        self.birth_date_label = tk.Label(self.register_window, text="Birth Date:", font=field_label_font)
        self.birth_date_label.grid(row=5, column=0, padx=10, pady=5)
        self.birth_date_entry = Calendar(self.register_window,selectmode="day",
                                         year=2023, month=9, day=18,
                                         date_pattern='y-mm-dd')
        self.birth_date_entry.grid(row=5, column=1, padx=10, pady=5)
        self.confirm_date = tk.Button(self.register_window, text='Select Date')

        self.register_button = tk.Button(self.register_window, text="Register", font=("Helvetica", 14), command=self.register)
        self.register_button.grid(row=6, columnspan=2, pady=10)

    def register(self):
        def clean_fields(name, last_name, password, id_number, birth_date):
            allowed_age = datetime.datetime.now() - datetime.timedelta(18 * 365)
            birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            if not all([name, last_name, password, id_number]):
                messagebox.showerror('Incorrect input', 'Please fill out all '
                                                        'the fields.')
                return False
            elif any(char.isdigit() for char in name) or any(char.isdigit() for char in last_name):
                messagebox.showerror('Incorrect field types', 'Please dont use '
                                                              'integers in name'
                                                              ' or last name '
                                                              'field.')
                return False
            elif not int(id_number):
                messagebox.showerror('Incorrect field types', 'ID number should'
                                                              ' be an integer')
                return False
            elif len(password) < 8:
                messagebox.showerror('Weak password', 'Password should be at '
                                                      'least 8 characters long')
                return False
            elif birth_date > allowed_age:
                messagebox.showerror("Too young", 'You should be at least 18 '
                                                  'years old to create a bank'
                                                  'account.')
                return False
            return True
        # Get user data from the form fields
        name = self.name_entry.get().title()
        last_name = self.last_name_entry.get().title()
        password = self.password_entry.get()
        birth_date = self.birth_date_entry.get_date()
        id_number = self.id_number_entry.get()

        database = 'bank.db'
        conn = create_connection(database)
        if clean_fields(name, last_name, password, id_number, birth_date):
            try:
                #Create a new user
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
                stored = hashed.decode('utf-8')
                print(hashed)
                create_user(conn, id_number, name, last_name, stored, birth_date, balance=0)

                # Reopen connection to database because create_user closed it
                conn = create_connection(database)
                user = login_user(conn, name, last_name, id_number, password)
                print(name, last_name, password)
                # Close the registration window
                self.register_window.destroy()

                # Show the bank menu in the parent window
                self.bank_app.show_bank_menu(user)
            # If password is not UNIQUE
            except sqlite3.IntegrityError:
                messagebox.showerror(title='Credentials in use',
                                     message='Account with this ID or password'
                                             'already exists. Try again.')

    def show(self):
        self.register_window.deiconify()

# ...
