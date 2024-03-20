import tkinter as tk
import bcrypt
from database import create_connection, login_user, update_user
from tkinter import messagebox


class LoginWindow:
    def __init__(self, parent, bank_app):
        self.parent = parent
        self.bank_app = bank_app
        self.login_window = tk.Toplevel(parent)
        self.login_window.focus()
        self.login_window.title("Login")
        # self.login_window.geometry('320x200')
        self.login_window.configure(bg='#ECECEC')

        self.login_label = tk.Label(self.login_window, text="Login Form",
                                    font=("Helvetica", 18, "bold"),
                                    bg='#ECECEC')
        self.login_label.grid(row=0, columnspan=2, pady=10)


        field_label_font = ("Helvetica", 12)

        self.username_label = tk.Label(self.login_window, text="Username:",
                                       font=field_label_font, bg='#ECECEC')
        self.username_label.grid(row=1, column=0, padx=10,
                                 pady=5)
        self.username_entry = tk.Entry(self.login_window, font=field_label_font)
        self.username_entry.grid(row=1, column=1, padx=10,
                                 pady=5)
        self.username_entry.focus()

        self.last_name_label = tk.Label(self.login_window, text="Last Name:",
                                        font=field_label_font, bg='#ECECEC')
        self.last_name_label.grid(row=2, column=0, padx=10,
                                  pady=5)
        self.last_name_entry = tk.Entry(self.login_window,
                                        font=field_label_font)
        self.last_name_entry.grid(row=2, column=1, padx=10,
                                  pady=5)
        self.id_number_label = tk.Label(self.login_window, text='ID number:',
                                   font=field_label_font, bg='#ECECEC')
        self.id_number_label.grid(row=3, column=0, padx=10, pady=5)
        self.id_number_entry = tk.Entry(self.login_window,
                                   font=field_label_font)
        self.id_number_entry.grid(row=3, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.login_window, text="Password:",
                                       font=field_label_font, bg='#ECECEC')
        self.password_label.grid(row=4, column=0, padx=10,
                                 pady=5)
        self.password_entry = tk.Entry(self.login_window, show="*",
                                       font=field_label_font)
        self.password_entry.grid(row=4, column=1, padx=10,
                                 pady=5)

        self.login_button = tk.Button(self.login_window, text="Login",
                                      font=("Helvetica", 14),
                                      command=self.login)
        self.login_button.grid(row=5, columnspan=2, pady=10)


        # Password reset
        self.password_reset = tk.Button(self.login_window,
                                        text='Forgot password?',
                                        command=self.reset_password)
        self.password_reset.grid(row=6, columnspan=2, pady= 10)

        self.login_window.bind('<Return>', lambda event=None: self.login())


    def login(self):
        def clean_fields(fields):
            if not all(fields):
                return False
            else:
                return True
        # Implement login logic here
        # For demonstration purposes, assume successful login
        user_name = self.username_entry.get().title()
        id_number = self.id_number_entry.get()
        password = self.password_entry.get()
        last_name = self.last_name_entry.get().title()
        if clean_fields([id_number, password]):

            database = 'bank.db'
            conn = create_connection(database)
            user = login_user(conn, user_name, last_name, id_number, password)
            if user:
                user_dict = user

                # Close the login window
                self.login_window.destroy()
                self.bank_app.show_bank_menu(user_dict)

        else:
            messagebox.showerror(title='Incorrect input',
                                 message='Please fill all the fields to log in'
                                         ' or create an account.')

        # Show the bank menu in the parent window

    def reset_password(self):
        def clean_fields():
            if len(username_entry.get())==0:
                messagebox.showerror(title='Incorrect input',
                                     message='Please write your username and'
                                             ' fill other fields')
            elif len(idnumber_entry.get())==0:
                messagebox.showerror(title='Incorrect input',
                                     message='Please write your ID number and'
                                             ' fill other fields')
            elif len(password1_entry.get())==0 and len(password2_entry.get())==0:
                messagebox.showerror(title='Incorrect input',
                                     message='Please write your Password in'
                                             'both fields and'
                                             ' fill other entries')
            elif password1_entry.get() != password2_entry.get():
                messagebox.showerror(title='Passwords are not matching',
                                     message='Passwords you provided are not '
                                             'matching each other, try again.')


        def confirm():
            username = username_entry.get().title()
            id_number = idnumber_entry.get()
            password = password2_entry.get()
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashed_for_db = hashed.decode('utf-8')
            database = 'bank.db'
            conn = create_connection(database)
            try:
                clean_fields()
            except:
                print('There was error, try again')
            finally:
                update_user(conn, username, id_number, hashed_for_db)
                reset_window.destroy()

        reset_window = tk.Toplevel(self.login_window)
        reset_window.title('Password reset')
        field_label_font = ("Helvetica", 12)

        title = tk.Label(reset_window,text='Reset your password',
                         font=field_label_font)
        title.grid(row=0, columnspan=2)

        username_label = tk.Label(reset_window, text='Username:',
                                  font=field_label_font)
        username_label.grid(row=1, column=0, pady=10, padx=5)
        username_entry = tk.Entry(reset_window, font=field_label_font)
        username_entry.grid(row=1, column=1, pady=10, padx=5)

        idnumber_label = tk.Label(reset_window, text='ID number:',
                                  font=field_label_font)
        idnumber_label.grid(row=2, column=0, pady=10, padx=5)
        idnumber_entry = tk.Entry(reset_window, font=field_label_font)
        idnumber_entry.grid(row=2, column=1, pady=10, padx=5)


        password1_label = tk.Label(reset_window, text='Password:'
                                   ,font=field_label_font)
        password1_label.grid(row=3, column=0, padx=10, pady=5)
        password1_entry = tk.Entry(reset_window, font=field_label_font, show='*')
        password1_entry.grid(row=3, column=1, padx=10, pady=5)

        password2_label = tk.Label(reset_window,
                                   text='Repeat:', font=field_label_font)
        password2_label.grid(row=4, column=0, padx=10, pady=5)
        password2_entry = tk.Entry(reset_window, font=field_label_font, show='*')
        password2_entry.grid(row=4, column=1, padx=10, pady=5)

        confirm_button = tk.Button(reset_window, text='Reset',
                                   font=field_label_font,
                                   command=confirm)
        confirm_button.grid(row=5, columnspan=2)

    def show(self):
        self.login_window.deiconify()
