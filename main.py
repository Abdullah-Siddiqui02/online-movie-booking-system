import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class MovieApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Movie Management System")
        self.root.geometry("850x550")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.title_var = tk.StringVar()
        self.director_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.rating_var = tk.StringVar()
        self.selected_item = None

        # --- HEADER ---
        header_frame = tk.Frame(root, bg="#3b5998")
        header_frame.pack(fill=tk.X)
        title_label = tk.Label(header_frame, text="My Movie Collection", 
                               font=("Segoe UI", 20, "bold"), bg="#3b5998", fg="white")
        title_label.pack(pady=15)

        # --- INPUT SECTION ---
        input_frame = tk.LabelFrame(root, text="Manage Movies", font=("Segoe UI", 12), bg="#f0f0f0", padx=10, pady=10)
        input_frame.pack(pady=15, padx=20, fill=tk.X)

        tk.Label(input_frame, text="Movie Title:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Director:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.director_var, width=30).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Year:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.year_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Rating (1-10):", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(input_frame, textvariable=self.rating_var, width=30).grid(row=1, column=3, padx=5, pady=5)

        # --- BUTTONS ---
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=5)
        btn_style = {"font": ("Segoe UI", 10, "bold"), "width": 15, "pady": 5}

        tk.Button(btn_frame, text="Add Movie", command=self.add_movie, bg="#4CAF50", fg="white", **btn_style).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Update", command=self.update_movie, bg="#2196F3", fg="white", **btn_style).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Delete", command=self.delete_movie, bg="#f44336", fg="white", **btn_style).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Clear", command=self.clear_text, bg="#9E9E9E", fg="white", **btn_style).grid(row=0, column=3, padx=10)

        # --- LIST VIEW ---
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        scroll = tk.Scrollbar(tree_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Director", "Year", "Rating"), show='headings', yscrollcommand=scroll.set)
        scroll.config(command=self.tree.yview)

        for col, width in [("ID", 50), ("Title", 250), ("Director", 200), ("Year", 100), ("Rating", 100)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.select_item)
        self.populate_list()

    def populate_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.db.fetch_all():
            self.tree.insert("", tk.END, values=row)

    def add_movie(self):
        if self.title_var.get() == "":
            messagebox.showerror("Error", "Title Required")
            return
        try:
            self.db.add_movie(self.title_var.get(), self.director_var.get(), int(self.year_var.get()), int(self.rating_var.get()))
            self.clear_text()
            self.populate_list()
        except ValueError:
             messagebox.showerror("Error", "Year/Rating must be numbers")

    def select_item(self, event):
        try:
            self.selected_item = self.tree.item(self.tree.selection())['values']
            self.title_var.set(self.selected_item[1])
            self.director_var.set(self.selected_item[2])
            self.year_var.set(self.selected_item[3])
            self.rating_var.set(self.selected_item[4])
        except IndexError: pass

    def delete_movie(self):
        if not self.selected_item: return
        self.db.remove_movie(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    def update_movie(self):
        if not self.selected_item: return
        try:
            self.db.update_movie(self.selected_item[0], self.title_var.get(), self.director_var.get(), int(self.year_var.get()), int(self.rating_var.get()))
            self.clear_text()
            self.populate_list()
        except ValueError: pass

    def clear_text(self):
        self.title_var.set(""); self.director_var.set(""); self.year_var.set(""); self.rating_var.set(""); self.selected_item = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()