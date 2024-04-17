import tkinter as tk
from ast import main
from tkinter import messagebox
import sqlite3

def setup_database():
    conn = sqlite3.connect('userdatabase.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.is_logged_in = False  # Flag to track login status
        master.title("Login System")

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.pack(pady=5)

        master.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle close button

    def on_close(self):
        if not self.is_logged_in:
            messagebox.showinfo("Info", "Exiting: Not logged in.")
            self.master.destroy()  # Prevents continuation without login

    def register(self):
        new_window = tk.Toplevel(self.master)
        Register(new_window)

    def login(self):
        new_window = tk.Toplevel(self.master)
        Login(new_window, self)

class Register:
    def __init__(self, master):
        self.master = master
        master.title("Register")

        self.username_label = tk.Label(master, text="Enter new username:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(master, text="Enter new password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        self.register_button = tk.Button(master, text="Register", command=self.register_user)
        self.register_button.pack(pady=5)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = sqlite3.connect('userdatabase.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registration successful!")
            self.master.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

class Login:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        master.title("Login")

        self.username_label = tk.Label(master, text="Enter your username:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(master, text="Enter your password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(master, text="Login", command=self.login_user)
        self.login_button.pack(pady=5)

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.master.destroy()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('userdatabase.db')
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cur.fetchone()
        conn.close()

        if result and result[0] == password:
            messagebox.showinfo("Success", "Login successful!")
            self.app.is_logged_in = True
            self.master.destroy()
            self.app.master.destroy()  # Close the main window
        else:
            messagebox.showerror("Error", "Invalid username or password.")

if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()



    import tkinter as tk
    from tkinter import ttk, messagebox
    from PIL import Image, ImageTk
    import sqlite3
    import random

    class Database:
        def __init__(self, db_name="library.db"):
            self.conn = sqlite3.connect(db_name)
            self.create_table()

        def create_table(self):
            query = """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
            """
            self.conn.execute(query)
            self.conn.commit()

        def add_book(self, title, author):
            query = "INSERT INTO books (title, author) VALUES (?, ?)"
            self.conn.execute(query, (title, author))
            self.conn.commit()

        def get_books(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, title, author FROM books")
            return cursor.fetchall()

        def update_book(self, book_id, title, author):
            query = "UPDATE books SET title = ?, author = ? WHERE id = ?"
            self.conn.execute(query, (title, author, book_id))
            self.conn.commit()

        def delete_book(self, book_id):
            query = "DELETE FROM books WHERE id = ?"
            self.conn.execute(query, (book_id,))
            self.conn.commit()

    class Interface(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Library Management System - Al-Grabe3")
            self.geometry("800x600")
            self.database = Database()  # Initialize the database

            # Load the background image
            self.bg_image = Image.open("library_background.jpg")  # Adjust path as needed
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.create_widgets()

        def create_widgets(self):
            self.title_label = tk.Label(self, text="Welcome to Al-Grabe3 Library", font=("Arial", 24), bg="black",
                                        fg="white")
            self.title_label.pack(pady=20)

            self.menu_frame = tk.Frame(self, bg='black')
            self.menu_frame.pack(pady=20)

            buttons = [("Add Book", self.add_book),
                       ("Display Books", self.display_books),
                       ("Update Book", self.update_book),
                       ("Delete Book", self.delete_book),
                       ("Exit", self.quit)]

            for i, (text, command) in enumerate(buttons):
                button = tk.Button(self.menu_frame, text=text, command=command, width=15, fg="white", bg="black")
                button.grid(row=0, column=i, padx=10, pady=10)
                button.bind("<Enter>", self.on_enter)
                button.bind("<Leave>", self.on_leave)

        def on_enter(self, event):
            """Change background on mouse enter."""
            new_color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
            event.widget.config(bg=new_color)

        def on_leave(self, event):
            """Reset background on mouse leave."""
            event.widget.config(bg="black")

        def add_book(self):
            add_window = AddBookWindow(self)

        def display_books(self):
            display_window = DisplayBooksWindow(self)

        def update_book(self):
            update_window = UpdateBookWindow(self)

        def delete_book(self):
            delete_window = DeleteBookWindow(self)

    class AddBookWindow(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.title("Add Book")
            self.geometry("400x250")
            self.configure(background='black')

            self.title_label = tk.Label(self, text="Title:", bg='black', fg='white')
            self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.title_entry = tk.Entry(self, width=40)
            self.title_entry.grid(row=0, column=1, padx=10, pady=10)

            self.author_label = tk.Label(self, text="Author:", bg='black', fg='white')
            self.author_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            self.author_entry = tk.Entry(self, width=40)
            self.author_entry.grid(row=1, column=1, padx=10, pady=10)

            self.add_button = tk.Button(self, text="Add Book", command=self.add_book, width=15, fg="white", bg="black")
            self.add_button.grid(row=2, columnspan=2, padx=10, pady=10)

        def add_book(self):
            title = self.title_entry.get()
            author = self.author_entry.get()
            if title and author:
                self.master.database.add_book(title, author)
                messagebox.showinfo("Success", "Book added successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Please enter both title and author.")

    class DisplayBooksWindow(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.title("Display Books")
            self.geometry("800x400")
            self.configure(background='black')

            self.books_tree = ttk.Treeview(self, columns=("ID", "Title", "Author"), show="headings")
            self.books_tree.heading("ID", text="ID")
            self.books_tree.heading("Title", text="Title")
            self.books_tree.heading("Author", text="Author")
            self.books_tree.pack(fill=tk.BOTH, expand=True)

            self.display_books()

        def display_books(self):
            self.books_tree.delete(*self.books_tree.get_children())
            books = self.master.database.get_books()
            for book in books:
                self.books_tree.insert("", "end", values=book)

    class UpdateBookWindow(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.title("Update Book")
            self.geometry("400x300")
            self.configure(background='black')

            self.book_id_label = tk.Label(self, text="Book ID:", bg='black', fg='white')
            self.book_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.book_id_entry = tk.Entry(self, width=40)
            self.book_id_entry.grid(row=0, column=1, padx=10, pady=10)

            self.title_label = tk.Label(self, text="Title:", bg='black', fg='white')
            self.title_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            self.title_entry = tk.Entry(self, width=40)
            self.title_entry.grid(row=1, column=1, padx=10, pady=10)

            self.author_label = tk.Label(self, text="Author:", bg='black', fg='white')
            self.author_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            self.author_entry = tk.Entry(self, width=40)
            self.author_entry.grid(row=2, column=1, padx=10, pady=10)

            self.update_button = tk.Button(self, text="Update Book", command=self.update_book, width=15, fg="white",
                                           bg="black")
            self.update_button.grid(row=3, columnspan=2, padx=10, pady=10)

        def update_book(self):
            book_id = self.book_id_entry.get()
            title = self.title_entry.get()
            author = self.author_entry.get()
            if book_id and title and author:
                self.master.database.update_book(book_id, title, author)
                messagebox.showinfo("Success", "Book updated successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Please fill out all fields.")

    class DeleteBookWindow(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.title("Delete Book")
            self.geometry("400x250")
            self.configure(background='black')

            self.book_id_label = tk.Label(self, text="Book ID:", bg='black', fg='white')
            self.book_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.book_id_entry = tk.Entry(self, width=40)
            self.book_id_entry.grid(row=0, column=1, padx=10, pady=10)

            self.delete_button = tk.Button(self, text="Delete Book", command=self.delete_book, width=15, fg="white",
                                           bg="black")
            self.delete_button.grid(row=1, columnspan=2, padx=10, pady=10)

        def delete_book(self):
            book_id = self.book_id_entry.get()
            if book_id:
                self.master.database.delete_book(book_id)
                messagebox.showinfo("Success", "Book deleted successfully.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Please enter the book ID.")

    if __name__ == "__main__":
        app = Interface()
        app.mainloop()

    print("Program is closed...")


if __name__ == "__main__":
    main()