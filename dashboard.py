import tkinter as tk
import requests
from tkinter import messagebox
from tkinter.ttk import Treeview, Combobox
from tkcalendar import Calendar
from database import create_connection, update_balance, \
    create_transaction, get_transactions, money_transfer, update_user


class DashboardApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        database = 'bank.db'
        self.conn = create_connection(database)
        self.root.title("Bank Application")
        self.initialize_main_window()


    def initialize_main_window(self):
        self.root.geometry('700x600')
        self.root.configure(bg="#F0F0F0")
        self.label_style = ("Helvetica", 16, "bold")
        self.button_style = ("Helvetica", 14, "bold")
        self.button_width = 10


        self.label = tk.Label(self.root, text=f"Hello {self.user.get('name')}",
                              font=self.label_style, bg="#F0F0F0")
        self.label.grid(row=0, pady=10, padx=300, columnspan=3)

        self.balance = tk.Label(self.root,
                                text=f'Your balance {self.user.get("balance")}',
                                font=self.label_style, bg="#F0F0F0")
        self.balance.grid(row=1, column=0)

        self.deposit_button = tk.Button(self.root, text='deposit money',
                                        command=self.deposit_window,
                                        font=self.label_style, bg="#F0F0F0")
        self.deposit_button.grid(row=1, column=1, sticky='N')

        self.withdraw_label = tk.Label(self.root, text='Withdraw money',
                                       font=self.label_style, bg="#F0F0F0")
        self.withdraw_label.grid(row=2, column=0)
        self.withdraw_button = tk.Button(self.root, text='Withdraw',
                                         command=self.withdraw_window,
                                         font=self.label_style, bg="#F0F0F0")
        self.withdraw_button.grid(row=2, column=1)

        self.transaction_label = tk.Label(self.root, text='Transaction history',
                                          font=self.label_style, bg="#F0F0F0")
        self.transaction_label.grid(row=3, column=0)
        self.transaction_button = tk.Button(self.root, text='See transactions',
                                            command=self.transaction_window,
                                            font=self.label_style, bg="#F0F0F0")
        self.transaction_button.grid(row=3, column=1)

        self.send_to_label = tk.Label(self.root, text='Send money to others',
                                      font=self.label_style, bg="#F0F0F0")
        self.send_to_label.grid(row=4, column=0)
        self.send_to_button = tk.Button(self.root, text='Find and send',
                                        command=self.send_money_window,
                                        font=self.label_style, bg="#F0F0F0")
        self.send_to_button.grid(row=4, column=1)

        self.profile_label = tk.Label(self.root, text='Check/Edit your profile',
                                      font=self.label_style, bg="#F0F0F0")
        self.profile_label.grid(row=5, column=0)
        self.profile_button = tk.Button(self.root, text='Profile',
                                        command=self.profile_window,
                                        font=self.label_style, bg="#F0F0F0")
        self.profile_button.grid(row=5, column=1)

        # Currency window opener
        self.currency_label = tk.Label(self.root, text='Check current curency',
                                       font=self.label_style, bg='#F0F0F0')
        self.currency_label.grid(row=6, column=0)
        self.currency_button = tk.Button(self.root, text='See currency',
                                         font=self.label_style, bg='#F0F0F0',
                                         command=self.currency_window)
        self.currency_button.grid(row=6, column=1)


        self.logout_button = tk.Button(self.root, text='Log Out',
                                       command=self.logout,
                                       font=self.label_style, bg="#F0F0F0"
                                       )
        self.logout_button.grid(row=7, column=0, columnspan=2)

    def logout(self):
        self.user = None
        self.conn.close()
        self.root.destroy()

    def deposit_window(self):
        # Deposit into account and create corresponding transaction
        def deposit_balance():
            user_id = self.user.get('id')
            deposit_amount = new_balance_entry.get()
            if float(deposit_amount) > 0:
                conn = self.conn
                updated_user = update_balance(conn, user_id, float(deposit_amount))
                create_transaction(conn, user_id, ' deposited', deposit_amount)
                self.user = updated_user
                deposit_window.destroy()
                self.balance.configure(text=f'Your balance {self.user.get("balance")}')
            else:
                messagebox.showerror(title='Incorrect input', message='Please write correct number')
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title('Deposit money in your account')

        current_balance = tk.Label(deposit_window,
                                   text=f'Your balance '
                                        f'{self.user.get("balance")}',
                                   font=self.label_style, bg="#F0F0F0")
        current_balance.grid(row=0, column=0, pady=5, padx=10)

        new_balance_label = tk.Label(deposit_window,text='update your balance',
                                     font=self.label_style, bg="#F0F0F0")
        new_balance_label.grid(row=1, column=0, pady=5, padx=10)
        new_balance_entry = tk.Entry(deposit_window,width=15)
        new_balance_entry.grid(row=1, column=1, pady=5, padx=10)

        confirm = tk.Button(deposit_window,text='Deposit',
                            command=deposit_balance,
                            font=self.label_style, bg="#F0F0F0")
        confirm.grid(row=2, columnspan=2, pady=5, padx=10)

    def withdraw_window(self):
        # Withdraw from account and create corresponding transaction
        def withdraw_balance():
            withdraw_amount = float(withdraw_entry.get())
            user_id = self.user.get('id')
            balance = float(self.user.get('balance'))
            if balance > withdraw_amount:
                if float(withdraw_amount) > 0:
                    conn = self.conn
                    updated_user = update_balance(conn, user_id,
                                                  withdraw_amount,
                                                  withdraw=True)
                    create_transaction(conn, user_id, 'withdrawn',
                                       withdraw_amount)
                    self.user = updated_user
                    withdraw_window.destroy()
                    self.balance.configure(text=f'Your balance '
                                                f'{self.user.get("balance")}')
                else:
                    messagebox.showerror(title='Incorrect input',
                                         message='Please write correct number')
            else:
                messagebox.showerror(title='Insuficient balance',
                                     message='Please write correct withdraw amount')

        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title('Withdraw your money')

        current_balance = tk.Label(withdraw_window,
                                   text=f'Your balance '
                                        f'{self.user.get("balance")}',
                                   font=self.label_style, bg="#F0F0F0")
        current_balance.grid(row=0, column=0, pady=5, padx=10)

        withdraw_label = tk.Label(withdraw_window, text='Withdraw amount: ',
                                  font=self.label_style, bg="#F0F0F0")
        withdraw_label.grid(row=1, column=0, pady=5, padx=10)
        withdraw_entry = tk.Entry(withdraw_window, width=15,
                                  font=self.label_style, bg="#F0F0F0")
        withdraw_entry.grid(row=1, column=1, pady=5, padx=10)

        confirm = tk.Button(withdraw_window, text='Withdraw',
                            command=withdraw_balance,
                            font=self.label_style, bg="#F0F0F0")
        confirm.grid(row=2, columnspan=2, pady=5, padx=10)

    def transaction_window(self):
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title('Transaction history')

        tree = Treeview(transaction_window,
                        columns=('action_type', 'amount', 'date', 'from'),
                        show=['headings'])

        # Set the column headings
        tree.heading("#1", text="Action")
        tree.heading("#2", text="Amount")
        tree.heading("#3", text="Date")  # Corrected column heading
        tree.heading("#4", text="From user")

        conn = self.conn
        transactions = get_transactions(conn, self.user.get('id'))
        for row in transactions:
            cleaned_row = [value if value != 'from' else 'N/A' for value in row]
            tree.insert('', 'end', values=cleaned_row)

        # Pack the Treeview widget
        tree.grid(row=0, column=0, sticky=tk.NSEW)

    def send_money_window(self):
        def send_money():
            self_id = self.user.get('id')
            user_id = int(find_entry.get())
            amount = amount_entry.get()
            balance = self.user.get('balance')

            if len(amount) == 0:
                messagebox.showerror(title='Incorrect input',
                                     message='Please write transfer amount')
            elif float(amount) <= 0:
                messagebox.showerror(title='Incorrect input',
                                     message='Please write correct amount')
            elif float(amount) > balance:
                messagebox.showerror(title='Incorrect input',
                                     message='You dont have enough balance')
            else:
                conn = self.conn
                #Transfer money and get new user model for dashboard
                updated_user = money_transfer(conn, self_id, user_id, amount)
                if updated_user is not None:
                    create_transaction(conn, self_id, 'sent', amount, user_id)
                    create_transaction(conn, user_id, 'received', amount, self_id)
                    self.user = updated_user
                    self.balance.configure(text=f'Your balance '
                                                f'{self.user.get("balance")}',
                                           font=self.label_style, bg="#F0F0F0")
                    send_window.destroy()
                    messagebox.showinfo(title='Success',
                                        message='Money was transfered successfully')
                else:
                    send_window.destroy()

        send_window = tk.Toplevel(self.root)
        send_window.title('Send money to other users')

        label = tk.Label(send_window, text='Find user by their ID',
                         font=self.label_style, bg="#F0F0F0")
        label.grid(row=0, columnspan=2, padx=15)

        guide_label = tk.Label(send_window, text='Put ID and sending amount',
                               font=self.label_style, bg="#F0F0F0")
        guide_label.grid(row=1, columnspan=2, padx=15)
        find_label = tk.Label(send_window, text='ID',
                              font=self.label_style,
                              bg="#F0F0F0"
                              )
        find_label.grid(row=2, column=0, padx=15, pady=5)
        find_entry = tk.Entry(send_window, width=15,
                              font=self.label_style,bg="#F0F0F0")
        find_entry.grid(row=2, column=1, padx=15, pady=5)
        amount_label = tk.Label(send_window, text='Amount',
                                font=self.label_style,
                                bg="#F0F0F0"
                                )
        amount_label.grid(row=3, column=0, padx=15, pady=5)
        amount_entry = tk.Entry(send_window, width=15,
                                font=self.label_style,
                                bg="#F0F0F0"
                                )
        amount_entry.grid(row=3, column=1, padx=15, pady=5)

        confirm_button = tk.Button(send_window, text='Find & Send',
                                   command=send_money,
                                   font=self.label_style,
                                   bg="#F0F0F0"
                                   )
        confirm_button.grid(row=4, column=0, columnspan=2, pady=5)

    def profile_window(self):
        def clean_fields(fields):

            if not all(fields):
                messagebox.showerror('Incorrect input',
                                     'You cant save empty fields, please fill '
                                     'out everything')
            else:
                return True
        def confirm_update():
            conn = self.conn
            username = var_username.get()
            last_name = var_lastname.get()
            id_number = var_idnumber.get()
            date = date_entry.get_date()
            password = self.user.get('password')
            user_id = self.user.get('id')

            if clean_fields([username, last_name, id_number, date]):
                user = update_user(conn, username, id_number, password,
                                   last_name, date, user_id)
                conn.close()
                self.user = user
                profile_window.destroy()

        profile_window = tk.Toplevel(self.root)
        profile_window.title('Profile')

        # We use StringVar and IntVar because we need to
        # pass in variables to db call

        username = self.user.get('name')
        name_label = tk.Label(profile_window, text=f'UserName:',
                              font=self.label_style, bg="#F0F0F0")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        var_username = tk.StringVar(profile_window, value=username)
        name_entry = tk.Entry(profile_window, textvariable=var_username,
                              font=self.label_style, bg="#F0F0F0")
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        last_name = self.user.get('last_name')
        last_name_label = tk.Label(profile_window, text=f'Last Name:',
                                   font=self.label_style, bg="#F0F0F0")
        last_name_label.grid(row=1, column=0, pady=5, padx=10)
        var_lastname = tk.StringVar(profile_window, value=last_name)
        last_name_entry = tk.Entry(profile_window, textvariable=var_lastname,
                                   font=self.label_style, bg="#F0F0F0")
        last_name_entry.grid(row=1, column=1, pady=5, padx=10)

        id_number = self.user.get('id_number')
        id_label = tk.Label(profile_window, text=f'ID number:',
                            font=self.label_style, bg="#F0F0F0")
        id_label.grid(row=2, column=0, padx=10, pady=5)
        var_idnumber = tk.IntVar(profile_window, value=id_number)
        id_entry = tk.Entry(profile_window, textvariable=var_idnumber,
                            font=self.label_style, bg="#F0F0F0")
        id_entry.grid(row=2, column=1, padx=10, pady=5)

        date = self.user.get('birth_date')
        date_label = tk.Label(profile_window, text=f'Birth date:',
                              font=self.label_style, bg="#F0F0F0")
        date_label.grid(row=3, column=0, pady=5, padx=10)
        var_date = tk.StringVar(profile_window, value=date)
        date_entry = Calendar(profile_window, selectmode='day',
                              textvariable=var_date)
        date_entry.grid(row=3, column=1, pady=5, padx=10)

        confirm_button = tk.Button(profile_window, text='Confirm changes',
                                   font=self.label_style, bg="#F0F0F0",
                                   command=confirm_update)
        confirm_button.grid(row=4, column=0, padx=10, pady=5)
        go_back = tk.Button(profile_window, text='Dashboard',
                            font=self.label_style, bg="#F0F0F0",
                            command=lambda: profile_window.destroy())
        go_back.grid(row=4, column=1, pady=5, padx=10)

    def currency_window(self):
        def exchange():
            from_cur = from_currency.get()
            to_cur = to_currency.get()
            exchange_amount = amount.get()
            balance = self.user.get('balance')
            try:
                if to_cur != from_cur:
                    if exchange_amount < balance:
                        conn = self.conn

                        result = response['rates'][from_cur]*response['rates'][to_cur]*exchange_amount
                        user_id = self.user.get('id')

                        updated_user = update_balance(conn, user_id, exchange_amount, withdraw=True)

                        create_transaction(conn, action=f'exchanged to {to_cur}',
                                           amount=exchange_amount,
                                           user_id=user_id)
                        self.user = updated_user
                        self.balance.configure(text=f'Your balance '
                                                    f'{self.user.get("balance")}')
                        messagebox.showinfo('success', f'You bought {float(result)} {to_cur}')

                    else:
                        messagebox.showerror('Insufficient balance',
                                             'You dont have enough balance for this '
                                             'transaction')
                else:
                    messagebox.showerror('Incorrect currencies',
                                         'Please choose something other than '
                                         'USD')
            except tk.TclError:
                messagebox.showerror('Incorrect input',
                                     'Please write correct amount')

        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        response = requests.get(url).json()

        gel = response['rates']['GEL']
        euro = response['rates']['EUR']

        currency_window = tk.Toplevel(self.root)

        welcome_label = tk.Label(currency_window, text='Check current currencies',
                                 font=self.label_style, bg='#F0F0F0')
        welcome_label.grid(row=0, columnspan=2)
        balance_label = tk.Label(currency_window, text=f'Your balance: '
                                                       f'{self.user.get("balance")}')
        balance_label.grid(row=1, columnspan=2)

        gel = tk.Label(currency_window, text=f'1 USD is {gel} GEL',
                       font=self.label_style, bg='#F0F0F0')
        gel.grid(row=2, columnspan=2)
        euro = tk.Label(currency_window, text=f'1 USD is {euro} euro',
                       font=self.label_style, bg='#F0F0F0')
        euro.grid(row=3, columnspan=2)

        second_label = tk.Label(currency_window, text='You can search and buy'
                                                      ' any currency you want.',
                                font=self.label_style, bg='#F0F0F0')
        second_label.grid(row=4, columnspan=3)

        from_currency = tk.StringVar()
        from_currency_label = tk.Label(currency_window, text='From currency:',
                                       font=self.label_style, bg='#F0F0F0')
        from_currency_label.grid(row=5, column=0)
        from_currency_box = Combobox(currency_window, textvariable=from_currency,
                                     state='readonly',
                                     values=['USD'])
        from_currency_box.current(0)
        from_currency_box.grid(row=5, column=1)
        to_currency = tk.StringVar()
        to_currency_label = tk.Label(currency_window, text='To currency:',
                                       font=self.label_style, bg='#F0F0F0')
        to_currency_label.grid(row=6, column=0)
        to_currency_box = Combobox(currency_window, textvariable=to_currency,
                                     state='readonly',
                                     values=list(response['rates'].keys()),)
        to_currency_box.current(0)
        to_currency_box.grid(row=6, column=1)

        amount = tk.DoubleVar()
        amount_label = tk.Label(currency_window, text='Choose amount:',
                                font=self.label_style, bg='#F0F0F0')
        amount_label.grid(row=7, column=0)
        amount_entry = tk.Entry(currency_window, textvariable=amount,
                                font=self.label_style, bg='#F0F0F0')
        amount_entry.grid(row=7, column=1)

        exchange_button = tk.Button(currency_window, text='Exchange',
                                    font=self.label_style, bg='#F0F0F0',
                                    command=lambda: exchange())
        exchange_button.grid(row=8, columnspan=2)


