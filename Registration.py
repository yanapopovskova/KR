from tkinter import *
import tkinter.messagebox as messagebox
import os

def register_window():
    root.withdraw()  # Скрыть основное окно
    register_window = Toplevel(root)
    register_window.title("Регистрация")

    register_window_width = 300
    register_window_height = 300

    register_window_x = int((screen_width / 2) - (register_window_width / 2))
    register_window_y = int((screen_height / 2) - (register_window_height / 2))

    register_window.geometry(f"{register_window_width}x{register_window_height}+{register_window_x}+{register_window_y}")

    label_register_username = Label(register_window, text="Логин:", font=("Arial", 12))
    label_register_username.pack()
    entry_register_username = Entry(register_window)
    entry_register_username.pack()

    label_register_password = Label(register_window, text="Пароль:", font=("Arial", 12))
    label_register_password.pack()
    entry_register_password = Entry(register_window, show="*")
    entry_register_password.pack()

    label_register_confirm_password = Label(register_window, text="Подтверждение пароля:",  font=("Arial", 12))
    label_register_confirm_password.pack()
    entry_register_confirm_password = Entry(register_window, show="*")
    entry_register_confirm_password.pack()

    button_register = Button(register_window, text="Регистрация",  font=("Arial", 12), command=lambda: register(entry_register_username.get(), entry_register_password.get(), entry_register_confirm_password.get(), register_window))
    button_register.pack()


def register(username, password, confirm_password, register_window):
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    if password != confirm_password:
        messagebox.showerror("Ошибка", "Пароли не совпадают")
        return

    with open("data.txt", "a") as file:
        file.write(f"{username},{password}\n")

    messagebox.showinfo("Регистрация", "Регистрация прошла успешно")
    register_window.destroy()
    root.deiconify()  # Открыть окно входа


def login(username, password):
    if username == "" or password == "":
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
        return

    if not os.path.isfile("data.txt"):
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
        return

    with open("data.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if username == stored_username and password == stored_password:
                messagebox.showinfo("Вход", "Вход выполнен")
                root.destroy()  # Закрыть окно входа
                return

    messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

root = Tk()
root.title("Вход")

label_login_username = Label(root, text="Логин:", font=("Arial", 12))
label_login_username.pack()
entry_login_username = Entry(root)
entry_login_username.pack()

label_login_password = Label(root, text="Пароль:", font=("Arial", 12))
label_login_password.pack()
entry_login_password = Entry(root, show="*")
entry_login_password.pack()

button_login = Button(root, text="Вход",  font=("Arial", 12), command=lambda: login(entry_login_username.get(), entry_login_password.get()))
button_login.pack()

button_register = Button(root, text="Регистрация",  font=("Arial", 12), command=register_window)
button_register.pack()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (200 / 2))
y = int((screen_height / 2) - (200 / 2))

root.geometry(f"300x300+{x}+{y}")

previous_register_window = None

root.mainloop()
