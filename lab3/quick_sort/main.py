"""
GUI приложение для сортировки массивов алгоритмом Quick Sort.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import random
from quick_sort import quick_sort
from auth import AuthManager


class QuickSortApp:
    """Класс для работы с алгоритмом Quick Sort."""
    
    MAX_ARRAY_SIZE = 1000
    
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Sort - Сортировка массивов")
        self.root.geometry("800x600")
        
        # Менеджер аутентификации
        self.auth_manager = AuthManager()
        
        # Данные
        self.original_array = []
        self.sorted_array = None
        
        # Создаем интерфейс
        self.create_widgets()
        self.update_auth_status()
    
    def create_widgets(self):
        """Создает элементы интерфейса."""
        # Верхняя панель
        top_frame = tk.Frame(self.root, relief=tk.RAISED, bd=1)
        top_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(
            top_frame,
            text="Quick Sort - Быстрая сортировка",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10, pady=5)
        
        # Панель авторизации
        auth_frame = tk.Frame(top_frame)
        auth_frame.pack(side="right", padx=10, pady=5)
        
        self.auth_label = tk.Label(auth_frame, text="Не авторизован")
        self.auth_label.pack(side="left", padx=5)
        
        self.login_btn = tk.Button(auth_frame, text="Войти", command=self.show_login_dialog)
        self.login_btn.pack(side="left", padx=2)
        
        self.logout_btn = tk.Button(auth_frame, text="Выйти", command=self.logout, state="disabled")
        self.logout_btn.pack(side="left", padx=2)
        
        # Основной контент
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Левая панель
        left_frame = tk.LabelFrame(main_frame, text="Управление", padx=10, pady=10)
        left_frame.pack(side="left", fill="y", padx=(0, 5))
        
        # Кнопки ввода
        tk.Button(left_frame, text="Ввести массив", command=self.input_array, width=20).pack(pady=5)
        tk.Button(left_frame, text="Сгенерировать случайный", command=self.generate_random, width=20).pack(pady=5)
        tk.Button(left_frame, text="Загрузить из файла", command=self.load_from_file, width=20).pack(pady=5)
        
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Кнопка сортировки
        self.sort_btn = tk.Button(left_frame, text="Отсортировать", command=self.sort_array, 
                                  width=20, state="disabled", bg="lightgreen")
        self.sort_btn.pack(pady=5)
        
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # История
        tk.Label(left_frame, text="История:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.save_btn = tk.Button(left_frame, text="Сохранить результат", command=self.save_sort_result,
                                  width=20, state="disabled")
        self.save_btn.pack(pady=5)
        
        self.history_btn = tk.Button(left_frame, text="Просмотр истории", command=self.show_history,
                                     width=20, state="disabled")
        self.history_btn.pack(pady=5)
        
        # Правая панель
        right_frame = tk.LabelFrame(main_frame, text="Результаты", padx=10, pady=10)
        right_frame.pack(side="left", fill="both", expand=True)
        
        # Информация
        self.info_label = tk.Label(right_frame, text="Введите или загрузите массив", 
                                   relief=tk.SUNKEN, bd=1, anchor="w")
        self.info_label.pack(fill="x", pady=(0, 10))
        
        # Исходный массив
        orig_frame = tk.LabelFrame(right_frame, text="Исходный массив")
        orig_frame.pack(fill="both", expand=True, pady=5)
        
        self.original_text = ScrolledText(orig_frame, wrap="word", height=8)
        self.original_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.original_text.insert("1.0", "Массив не задан")
        self.original_text.config(state="disabled")
        
        # Отсортированный массив
        sorted_frame = tk.LabelFrame(right_frame, text="Отсортированный массив")
        sorted_frame.pack(fill="both", expand=True, pady=5)
        
        self.sorted_text = ScrolledText(sorted_frame, wrap="word", height=8)
        self.sorted_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.sorted_text.insert("1.0", "Результат появится после сортировки")
        self.sorted_text.config(state="disabled")
        
        # Нижняя панель
        bottom_frame = tk.Frame(self.root, relief=tk.RAISED, bd=1)
        bottom_frame.pack(fill="x", side="bottom", padx=5, pady=5)
        
        self.status_bar = tk.Label(bottom_frame, text="Готово", anchor="w")
        self.status_bar.pack(side="left", padx=10)
        
        tk.Button(bottom_frame, text="Справка", command=self.show_help).pack(side="right", padx=10, pady=2)
    
    def show_login_dialog(self):
        """Показывает диалог авторизации."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Авторизация")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Вход в систему", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(dialog, text="Имя пользователя:").pack(anchor="w", padx=20, pady=(10, 0))
        username_entry = tk.Entry(dialog, width=30)
        username_entry.pack(padx=20, pady=5)
        username_entry.focus()
        
        tk.Label(dialog, text="Пароль:").pack(anchor="w", padx=20, pady=(10, 0))
        password_entry = tk.Entry(dialog, width=30, show="*")
        password_entry.pack(padx=20, pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            success, msg = self.auth_manager.login(username, password)
            if success:
                dialog.destroy()
                self.update_auth_status()
                messagebox.showinfo("Успех", msg)
            else:
                messagebox.showerror("Ошибка", msg)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            success, msg = self.auth_manager.register(username, password)
            if success:
                messagebox.showinfo("Успех", msg)
                success, msg = self.auth_manager.login(username, password)
                if success:
                    dialog.destroy()
                    self.update_auth_status()
            else:
                messagebox.showerror("Ошибка", msg)
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Войти", command=login, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Регистрация", command=register, width=12).pack(side="left", padx=5)
        
        password_entry.bind("<Return>", lambda e: login())
    
    def update_auth_status(self):
        """Обновляет статус авторизации."""
        if self.auth_manager.is_authenticated():
            username = self.auth_manager.get_current_username()
            self.auth_label.config(text=f"Пользователь: {username}")
            self.login_btn.config(state="disabled")
            self.logout_btn.config(state="normal")
            self.history_btn.config(state="normal")
            self.status_bar.config(text=f"Авторизован: {username}")
        else:
            self.auth_label.config(text="Не авторизован")
            self.login_btn.config(state="normal")
            self.logout_btn.config(state="disabled")
            self.history_btn.config(state="disabled")
            self.status_bar.config(text="Готово")
    
    def sort_array(self):
        """Выполняет быструю сортировку."""
        if not self.original_array:
            messagebox.showwarning("Предупреждение", "Сначала введите массив!")
            return
        
        try:
            self.info_label.config(text="Выполняется сортировка...")
            self.root.update()
            
            self.sorted_array = quick_sort(self.original_array.copy())
            
            self.original_text.config(state="normal")
            self.original_text.delete("1.0", tk.END)
            self.original_text.insert("1.0", str(self.original_array))
            self.original_text.config(state="disabled")
            
            self.sorted_text.config(state="normal")
            self.sorted_text.delete("1.0", tk.END)
            self.sorted_text.insert("1.0", str(self.sorted_array))
            self.sorted_text.config(state="disabled")
            
            self.info_label.config(text=f"Сортировка завершена. Элементов: {len(self.sorted_array)}")
            self.save_btn.config(state="normal")
            messagebox.showinfo("Успех", "Массив отсортирован!")
        except Exception as e:
            self.info_label.config(text=f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", str(e))
    
    def logout(self):
        """Выполняет выход."""
        self.auth_manager.logout()
        self.update_auth_status()
        messagebox.showinfo("Выход", "Вы вышли из системы")
    
    def save_sort_result(self):
        """Сохраняет результат."""
        if not self.auth_manager.is_authenticated():
            messagebox.showwarning("Предупреждение", "Необходимо авторизоваться!")
            self.show_login_dialog()
            return
        
        if not self.original_array or self.sorted_array is None:
            messagebox.showwarning("Предупреждение", "Сначала выполните сортировку!")
            return
        
        user_id = self.auth_manager.get_current_user_id()
        success, msg = self.auth_manager.db.save_sort_history(
            user_id, self.original_array, self.sorted_array
        )
        
        if success:
            messagebox.showinfo("Успех", "Результат сохранен!")
        else:
            messagebox.showerror("Ошибка", msg)
    
    def show_history(self):
        """Показывает историю."""
        if not self.auth_manager.is_authenticated():
            messagebox.showwarning("Предупреждение", "Необходимо авторизоваться!")
            self.show_login_dialog()
            return
        
        user_id = self.auth_manager.get_current_user_id()
        history = self.auth_manager.db.get_sort_history(user_id)
        
        if not history:
            messagebox.showinfo("История", "История пуста")
            return
        
        window = tk.Toplevel(self.root)
        window.title("История сортировок")
        window.geometry("700x500")
        
        tk.Label(window, text=f"История сортировок ({len(history)} записей)", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # Список
        canvas = tk.Canvas(window)
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas)
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for idx, record in enumerate(history):
            card = tk.LabelFrame(frame, text=f"Запись #{len(history) - idx} | {record['created_at']}", 
                               padx=10, pady=5)
            card.pack(fill="x", padx=10, pady=5)
            
            orig = str(record['original_array'])
            if len(orig) > 80:
                orig = orig[:80] + "..."
            
            tk.Label(card, text=f"Исходный: {orig}", wraplength=600, justify="left").pack(anchor="w")
            
            def load(o=record['original_array'], s=record['sorted_array']):
                self.original_array = o
                self.sorted_array = s
                
                self.original_text.config(state="normal")
                self.original_text.delete("1.0", tk.END)
                self.original_text.insert("1.0", str(o))
                self.original_text.config(state="disabled")
                
                self.sorted_text.config(state="normal")
                self.sorted_text.delete("1.0", tk.END)
                self.sorted_text.insert("1.0", str(s))
                self.sorted_text.config(state="disabled")
                
                self.sort_btn.config(state="normal")
                self.save_btn.config(state="normal")
                self.info_label.config(text=f"Загружено из истории: {len(o)} элементов")
                window.destroy()
            
            tk.Button(card, text="Загрузить", command=load).pack(anchor="e", pady=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
    
    def show_help(self):
        """Показывает справку."""
        help_text = """Quick Sort - Справка

1. Авторизация:
   - Войдите или зарегистрируйтесь для сохранения истории

2. Ввод данных:
   - "Ввести массив" - введите числа через пробел
   - "Сгенерировать" - создайте случайный массив
   - "Загрузить из файла" - загрузите из .txt файла

3. Сортировка:
   - Нажмите "Отсортировать" для запуска Quick Sort
   - Сложность: O(n log n) в среднем

4. История:
   - Сохраняйте результаты
   - Просматривайте и загружайте предыдущие сортировки

Максимальный размер массива: 1000 элементов"""
        
        window = tk.Toplevel(self.root)
        window.title("Справка")
        window.geometry("450x350")
        
        tk.Label(window, text="Справка", font=("Arial", 12, "bold")).pack(pady=10)
        
        text = tk.Text(window, wrap="word", padx=10, pady=10)
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", help_text)
        text.config(state="disabled")
        
        tk.Button(window, text="Закрыть", command=window.destroy).pack(pady=10)
    
    def input_array(self):
        """Ввод массива."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Ввод массива")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        tk.Label(dialog, text=f"Введите числа через пробел (макс. {self.MAX_ARRAY_SIZE}):").pack(pady=10)
        
        entry = tk.Entry(dialog, width=50)
        entry.pack(padx=10, pady=5)
        entry.focus()
        
        def ok():
            try:
                arr = [int(x) for x in entry.get().strip().split()]
                if not arr:
                    messagebox.showerror("Ошибка", "Массив пуст!")
                elif len(arr) > self.MAX_ARRAY_SIZE:
                    messagebox.showerror("Ошибка", f"Максимум {self.MAX_ARRAY_SIZE} элементов!")
                else:
                    self.original_array = arr
                    self.sorted_array = None
                    
                    self.original_text.config(state="normal")
                    self.original_text.delete("1.0", tk.END)
                    self.original_text.insert("1.0", str(arr))
                    self.original_text.config(state="disabled")
                    
                    self.sorted_text.config(state="normal")
                    self.sorted_text.delete("1.0", tk.END)
                    self.sorted_text.insert("1.0", "Готово к сортировке")
                    self.sorted_text.config(state="disabled")
                    
                    self.sort_btn.config(state="normal")
                    self.save_btn.config(state="disabled")
                    self.info_label.config(text=f"Загружено: {len(arr)} элементов")
                    dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите только целые числа!")
        
        tk.Button(dialog, text="OK", command=ok).pack(pady=10)
        entry.bind("<Return>", lambda e: ok())
    
    def generate_random(self):
        """Генерация случайного массива."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Генерация массива")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Параметры генерации", font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Label(dialog, text="Размер массива:").pack(anchor="w", padx=20)
        size_entry = tk.Entry(dialog, width=20)
        size_entry.pack(padx=20, pady=2)
        size_entry.insert(0, "20")
        
        tk.Label(dialog, text="Минимальное значение:").pack(anchor="w", padx=20, pady=(10, 0))
        min_entry = tk.Entry(dialog, width=20)
        min_entry.pack(padx=20, pady=2)
        min_entry.insert(0, "1")
        
        tk.Label(dialog, text="Максимальное значение:").pack(anchor="w", padx=20, pady=(10, 0))
        max_entry = tk.Entry(dialog, width=20)
        max_entry.pack(padx=20, pady=2)
        max_entry.insert(0, "100")
        
        def generate():
            try:
                size = int(size_entry.get())
                min_val = int(min_entry.get())
                max_val = int(max_entry.get())
                
                if size <= 0 or size > self.MAX_ARRAY_SIZE:
                    messagebox.showerror("Ошибка", f"Размер: 1-{self.MAX_ARRAY_SIZE}")
                    return
                if min_val > max_val:
                    messagebox.showerror("Ошибка", "Минимум больше максимума!")
                    return
                
                self.original_array = [random.randint(min_val, max_val) for _ in range(size)]
                self.sorted_array = None
                
                self.original_text.config(state="normal")
                self.original_text.delete("1.0", tk.END)
                self.original_text.insert("1.0", str(self.original_array))
                self.original_text.config(state="disabled")
                
                self.sorted_text.config(state="normal")
                self.sorted_text.delete("1.0", tk.END)
                self.sorted_text.insert("1.0", "Готово к сортировке")
                self.sorted_text.config(state="disabled")
                
                self.sort_btn.config(state="normal")
                self.save_btn.config(state="disabled")
                self.info_label.config(text=f"Сгенерировано: {size} элементов")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите числа!")
        
        tk.Button(dialog, text="Сгенерировать", command=generate).pack(pady=15)
    
    def load_from_file(self):
        """Загрузка из файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    numbers = []
                    for line in content.split("\n"):
                        numbers.extend([int(x) for x in line.split() if x.strip()])
                    
                    if not numbers:
                        messagebox.showerror("Ошибка", "Файл пуст!")
                    elif len(numbers) > self.MAX_ARRAY_SIZE:
                        messagebox.showerror("Ошибка", f"Максимум {self.MAX_ARRAY_SIZE} элементов!")
                    else:
                        self.original_array = numbers
                        self.sorted_array = None
                        
                        self.original_text.config(state="normal")
                        self.original_text.delete("1.0", tk.END)
                        self.original_text.insert("1.0", str(numbers))
                        self.original_text.config(state="disabled")
                        
                        self.sorted_text.config(state="normal")
                        self.sorted_text.delete("1.0", tk.END)
                        self.sorted_text.insert("1.0", "Готово к сортировке")
                        self.sorted_text.config(state="disabled")
                        
                        self.sort_btn.config(state="normal")
                        self.save_btn.config(state="disabled")
                        self.info_label.config(text=f"Загружено: {len(numbers)} элементов")
            except ValueError:
                messagebox.showerror("Ошибка", "Файл должен содержать только целые числа!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))


def main():
    root = tk.Tk()
    app = QuickSortApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()