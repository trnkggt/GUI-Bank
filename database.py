import sqlite3
import bcrypt
from sqlite3 import Error
from utils import dictify
from tkinter import messagebox
from datetime import datetime

# To create a db, we need Connection object
# That represents the database using connect()


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """
    create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: CREATE TABLE STATEMENT
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "bank.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY,
                                        id_number INTEGER UNIQUE CHECK(id_number >= 0),
                                        name TEXT NOT NULL,
                                        last_name TEXT NOT NULL,
                                        password TEXT(250) UNIQUE NOT NULL,
                                        birth_date TEXT NOT NULL,
                                        balance REAL NOT NULL
                                    ); """

    sql_create_transactions_table = """CREATE TABLE transactions (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        user_id INTEGER NOT NULL,
                                        action TEXT NOT NULL,
                                        amount DECIMAL(10, 2) NOT NULL,
                                        "from" TEXT,
                                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE                                
                                    );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)

        create_table(conn, sql_create_transactions_table)
    else:
        print('Error! cannot create database connection')


def create_user(conn, id_number, name, last_name, password, birth_date, balance=0):
    """
        Create an user if all this fields are populated correctly
    :param conn:
    :param id_number:
    :param name:
    :param last_name:
    :param password:
    :param birth_date:
    :param balance:
    :return:
    """
    sql = ''' INSERT INTO users(id_number, name, last_name, password, birth_date, balance) VALUES(?,?,?,?,?,?)'''
    user_data = (id_number, name, last_name, password, birth_date, balance)
    cur = conn.cursor()
    cur.execute(sql, user_data)
    conn.commit()
    user = cur.lastrowid
    conn.close()
    return user


def login_user(conn, user_name, last_name, id_number, password):
    """
    retrieve and login user
    :param conn:
    :param name:
    :param password:
    :return:
    """
    try:
        retrieve_user_sql = """SELECT * FROM users WHERE id_number = ? AND name = ? AND last_name = ?"""
        user_data = (id_number, user_name, last_name)
        cur = conn.cursor()
        cur.execute(retrieve_user_sql, user_data)

        user = cur.fetchone()
        conn.close()
        if user:
            # Retrieve user using provided name last name and id
            # using bcrypt.checkpw we check saved hash password against
            # user provided plain text password

            stored_hashed_password = user[4]  # Extract the stored hashed password from the user's row
            user_pass = password.encode('utf-8')
            if bcrypt.checkpw(user_pass, stored_hashed_password.encode('utf-8')):
                # Authentication successful
                print("Authentication successful.")
                return dictify(user) # You can return the user data for further use
            else:
                messagebox.showerror('Incorrect password',
                                     'Password you provided is not '
                                     'correct')
        else:
            # Authentication failed
            print("Authentication failed. Invalid username or password.")
            messagebox.showerror('Authentication failed.',
                                 'Invalid username or password')
            return None

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None

    except Exception as e:
        print("Error:", e)
        return None


def update_balance(conn, id, balance, withdraw=False):
    """
    update balance corresponding to users wish deposit/withdraw
    :param conn:
    :param id:
    :param balance:
    :return:
    """
    try:
        balance_retrieve = """SELECT balance FROM users WHERE id = ?"""
        cur = conn.cursor()
        cur.execute(balance_retrieve, (int(id),))
        old_balance = cur.fetchone()
        if old_balance is not None:
            old_balance = old_balance[0]
            if withdraw != False:
                updated_balance = old_balance - balance
            else:
                updated_balance = balance + old_balance
            cur.execute('UPDATE users SET balance = ? WHERE id = ?', (updated_balance, id))
            conn.commit()
            cur.execute('SELECT * FROM users WHERE id = ?', (int(id),))
            user = cur.fetchone()
            conn.close()
            return dictify(user)
    except sqlite3.Error as e:
        print(e)


def update_user(conn, user_name, id_number,
                password, last_name=None, birth_date=None, user_id=None):
    """
    Update user from profile or password change
    :param conn:
    :param user_name:
    :param id_number:
    :param password:
    :param last_name:
    :param birth_date:
    :param user_id:
    :return:
    """
    try:
        if all(var is None for var in (last_name, birth_date, user_id)):
            cur = conn.cursor()
            update_sql = "UPDATE users SET password = ? WHERE name = ? AND id_number = ?"
            cur.execute(update_sql, (password, user_name, id_number))
            conn.commit()
            conn.close()
            return True
        else:
            cur = conn.cursor()
            update_sql = 'UPDATE users SET id_number = ?, name = ?, last_name = ?, birth_date = ? WHERE id = ?'
            cur.execute(update_sql, (id_number, user_name, last_name, birth_date
                                     , user_id))
            conn.commit()
            cur.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
            user = cur.fetchone()
            conn.close()
            return dictify(user)
    except sqlite3.Error as e:
        print('SQLite error: ', e)




def create_transaction(conn, user_id, action, amount, from_user=None):
    """
    Create transaction based on users action deposit/withdraw
    :param conn:
    :param user_id:
    :param action:
    :param amount:
    :return:
    """
    try:
        if from_user is None:
            transaction_sql = """INSERT INTO transactions(user_id, action, amount) VALUES(?,?,?)"""
            data = (user_id, action, amount)
            cur = conn.cursor()
            cur.execute(transaction_sql, data)
            conn.commit()
            conn.close()
        else:
            transaction_sql = """INSERT INTO transactions(user_id, action, amount, 'from') VALUES(?,?,?,?)"""
            data = (user_id, action, amount, from_user)
            cur = conn.cursor()
            cur.execute(transaction_sql, data)
            conn.commit()
            conn.close()
    except sqlite3.Error as e:
        print(e)


def get_transactions(conn, user_id):
    cur = conn.cursor()
    # Updated sql query lets us filter and sort queryset
    cur.execute("SELECT action, amount, date, 'from' FROM transactions WHERE user_id = ? ORDER BY date DESC LIMIT 10", (user_id,))
    transactions = cur.fetchall()

    # We need to sort transactions based on date field
    # sorted_transactions = sorted(transactions, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'), reverse=True)

    return transactions


def money_transfer(conn, current_user_id, to_user_id, amount):
    try:
        cur = conn.cursor()

        cur.execute('SELECT id_number FROM users WHERE id_number = ?',
                       (to_user_id,))
        recipient = cur.fetchone()

        if recipient is None:
            messagebox.showerror('User error', 'User not found, please try again.')
            return None

        #Update current users balance
        cur.execute('UPDATE users SET balance = balance - ? WHERE id = ?',
                     (float(amount), current_user_id))
        #Send and update receiver users balance
        cur.execute('UPDATE users SET balance = balance + ? WHERE id_number = ?',
                     (float(amount), to_user_id))
        cur.execute('SELECT * FROM users WHERE id = ?', (current_user_id,))
        user = cur.fetchone()
        conn.commit()
        conn.close()
        return dictify(user)
    except sqlite3.Error as e:
        print('SQLite error: ', e)

if __name__ == '__main__':
    main()