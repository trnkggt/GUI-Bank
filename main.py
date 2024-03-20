import tkinter as tk
from register import RegisterWindow
from login import LoginWindow
from dashboard import DashboardApp

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        self.initialize_main_window()

    def initialize_main_window(self):

        self.root.configure(bg="#F0F0F0")
        self.label_style = ("Helvetica", 16, "bold")
        self.button_style = ("Helvetica", 14, "bold")
        self.button_width = 15

        self.label = tk.Label(self.root, text="Hello to my bank",
                              font=self.label_style, bg="#F0F0F0")
        self.label.grid(row=0, column=0, pady=20, columnspan=2)

        self.register_button = tk.Button(self.root, text="Register",
                                         font=self.button_style,
                                         width=self.button_width,
                                         command=self.open_register_window)
        self.register_button.grid(row=1, column=0, padx=10, pady=10)

        self.login_button = tk.Button(self.root, text="Login",
                                      font=self.button_style,
                                      width=self.button_width,
                                      command=self.open_login_window)
        self.login_button.grid(row=1, column=1, padx=10, pady=10)

    def open_register_window(self):
        self.register_window = RegisterWindow(self.root, self)
        self.register_window.show()

    def open_login_window(self):
        self.login_window = LoginWindow(self.root, self)
        self.login_window.show()

    def show_bank_menu(self, user):
        # Implement the bank menu content or window transition here
        self.label.destroy()
        self.login_button.destroy()
        self.register_button.destroy()
        DashboardApp(self.root, user)





def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
