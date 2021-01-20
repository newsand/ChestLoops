# greetings to https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
try:
    import Tkinter as tk

except:
    import tkinter as tk
import Configleton
from MainWindow import *
from User import User
from tkinter import Label, messagebox, Entry, Button
from AppViewPage import AppViewPage
BGC = Configleton.shared_instance().get_required_config_var("BGC")


class LoginPage(tk.Frame):
    def login(self):
        self.master.switch_frame(AppViewPage).pack()

    def __init__(self, master):
        self.usernameS = tk.StringVar()
        self.passwordS = tk.StringVar()
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg=BGC)
        tk.Label(self, text="Login", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        user_label = Label(self, text="User", bg=BGC, fg="white")
        user_label.pack()
        user_entry = Entry(self, textvariable=self.usernameS)
        user_entry.pack()
        pass_label = Label(self, text="Password", bg=BGC, fg="white")
        pass_label.pack()
        pass_entry = Entry(self, show="*", textvariable=self.passwordS)
        pass_entry.pack()
        login_button = Button(self, text="Login", command=self.validate)
        login_button.pack()
        print(Configleton.shared_instance().get_cryptokey())

    def validate(self):
        username = self.usernameS.get()
        password = self.passwordS.get()
        data = (username,)
        #print(1)
        #print(data)
        inputData = (username, password,)
        #print(2)
        #print(inputData)

        user_table = User()
        try:
            if user_table.validateData(data, inputData):
                Configleton._USER = user_table.get_id(data)
                messagebox.showinfo("Successful", "Login Was Successful")
                self.login()
            else:
                messagebox.showerror("Error", "Wrong Credentials")
        except IndexError:
            messagebox.showerror("Error", "Wrong Credentials")
        user_table.finish()