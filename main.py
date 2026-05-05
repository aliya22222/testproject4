import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import string

# Имя файла для хранения истории паролей
HISTORY_FILE = 'passwords_history.json'

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохранение нового пароля в историю
def save_password(password):
    history = load_history()
    history.append(password)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

# Генерация пароля
def generate_password(length, use_digits, use_letters, use_symbols):
    if not (use_digits or use_letters or use_symbols):
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов.")
        return None
    if length < 4 or length > 32:
        messagebox.showwarning("Ошибка", "Длина пароля должна быть от 4 до 32 символов.")
        return None
    charset = ''
    if use_digits:
        charset += string.digits
    if use_letters:
        charset += string.ascii_letters
    if use_symbols:
        charset += string.punctuation
    password = ''.join(random.choice(charset) for _ in range(length))
    return password

# Обновление таблицы истории
def update_history():
    for item in tree.get_children():
        tree.delete(item)
    history = load_history()
    for pw in history:
        tree.insert('', 'end', values=(pw,))

# Обработчик кнопки генерации
def on_generate():
    length = length_var.get()
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_symbols = var_symbols.get()

    pw = generate_password(length, use_digits, use_letters, use_symbols)
    if pw:
        save_password(pw)
        update_history()
        result_var.set(pw)

# Создаем главное окно
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("700x500")

# Ползунок длины пароля
tk.Label(root, text="Длина пароля").pack(pady=5)
length_var = tk.IntVar(value=12)
scale = tk.Scale(root, from_=4, to=32, orient='horizontal', variable=length_var)
scale.pack(pady=5)

# Чекбоксы для выбора символов
frame_checks = tk.Frame(root)
frame_checks.pack(pady=5)

var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(frame_checks, text="Цифры", variable=var_digits).pack(side='left', padx=10)
tk.Checkbutton(frame_checks, text="Буквы", variable=var_letters).pack(side='left', padx=10)
tk.Checkbutton(frame_checks, text="Спецсимволы", variable=var_symbols).pack(side='left', padx=10)

# Кнопка генерации
btn_generate = tk.Button(root, text="Генерировать", command=on_generate)
btn_generate.pack(pady=10)

# Отображение сгенерированного пароля
result_var = tk.StringVar()
tk.Label(root, text="Созданный пароль:", font=('Arial', 12)).pack()
tk.Entry(root, textvariable=result_var, font=('Arial', 14), width=50, justify='center').pack(pady=5)

# Таблица истории
tk.Label(root, text="История паролей").pack(pady=5)
columns = ('Password',)
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
tree.heading('Password', text='Пароль')
tree.pack(fill='both', expand=True, padx=10, pady=5)

# Загрузить историю при запуске
update_history()

# Запуск GUI
root.mainloop()